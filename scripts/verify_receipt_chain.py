"""Offline full-lineage verification against externally trusted anchors/keys."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nacl.signing import VerifyKey
from gate_zero_wire import SecurityException, parse_time, verify, verify_decision


def verify_chain(receipts, adapter_pubkeys, *, authorizations, decisions,
                 gatekeeper_pubkey_hex, genesis_receipt_hash,
                 genesis_state_hash, expected_head_hash):
    gatekeeper = VerifyKey(bytes.fromhex(gatekeeper_pubkey_hex))
    previous, state = genesis_receipt_hash, genesis_state_hash
    seen_auth, seen_nonce, seen_receipts = set(), set(), set()
    for receipt in receipts:
        adapter = receipt.get('adapter_id')
        if adapter not in adapter_pubkeys:
            raise SecurityException('unknown-adapter-key')
        verify('receipt', receipt, VerifyKey(bytes.fromhex(adapter_pubkeys[adapter])))
        auth_hash = receipt['authorization_hash']
        auth = authorizations.get(auth_hash)
        if auth is None:
            raise SecurityException('missing-authorization')
        verify('authorization', auth, gatekeeper)
        decision = decisions.get(auth['decision_hash'])
        if decision is None:
            raise SecurityException('missing-decision')
        verify_decision(decision)
        if decision['verdict'] != 'ALLOW':
            raise SecurityException('decision-not-allow')
        for a,d in [('decision_id','decision_id'),('decision_hash','decision_hash'),
                    ('request_hash','request_hash'),('adapter_id','target_adapter')]:
            if auth[a] != decision[d]:
                raise SecurityException('decision-binding-mismatch')
        for field in ('authorization_id','authorization_hash','adapter_id','parent_record_hash'):
            if receipt[field] != auth[field]:
                raise SecurityException('receipt-authorization-mismatch')
        start, end = parse_time(receipt['execution_start']), parse_time(receipt['timestamp'])
        issued, expiry = parse_time(auth['issued_at']), parse_time(auth['valid_until'])
        if not issued <= start < expiry or end < start or not 0 < (expiry-issued).total_seconds() <= 300:
            raise SecurityException('execution-time-invalid')
        if (auth_hash in seen_auth or auth['nonce'] in seen_nonce or
                receipt['ledger_entry_id'] in seen_receipts):
            raise SecurityException('chain-replay')
        seen_auth.add(auth_hash)
        seen_nonce.add(auth['nonce'])
        seen_receipts.add(receipt['ledger_entry_id'])
        if receipt['previous_receipt_hash'] != previous:
            raise SecurityException('broken-receipt-chain')
        if receipt['parent_record_hash'] != state:
            raise SecurityException('state-root-discontinuity')
        previous, state = receipt['receipt_hash'], receipt['resulting_record_hash']
        if state is None and receipt is not receipts[-1]:
            raise SecurityException('unknown-state-followed-by-execution')
    if previous != expected_head_hash:
        raise SecurityException('head-checkpoint-mismatch')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', help='JSON with receipts, authorizations and decisions')
    parser.add_argument('trust', help='Externally trusted keys, genesis roots and expected head')
    args = parser.parse_args()
    try:
        bundle = json.loads(Path(args.bundle).read_text())
        trust = json.loads(Path(args.trust).read_text())
        verify_chain(bundle['receipts'], authorizations=bundle['authorizations'],
                     decisions=bundle['decisions'], **trust)
    except (SecurityException, ValueError, KeyError, TypeError) as exc:
        print('Chain Verification: FAIL (' + str(exc) + ')')
        return 1
    print('Chain Verification: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
