import copy
import json
from pathlib import Path
import sys
import pytest
from nacl.signing import SigningKey
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'scripts')]
from gate_zero_wire import SecurityException,seal
from verify_receipt_chain import verify_chain


@pytest.fixture
def bundle():
    root=Path(__file__).parent/'fixtures'
    return json.loads((root/'boundary-bundle.json').read_text()),json.loads((root/'boundary-trust.json').read_text())


def audit(data,trust):
    return verify_chain(data['receipts'],authorizations=data['authorizations'],decisions=data['decisions'],**trust)


def test_complete_lineage_passes(bundle):
    assert audit(*bundle)


def test_broken_receipt_chain_fails_even_with_valid_signature(bundle):
    data,trust=bundle
    data['receipts'][1]['previous_receipt_hash']='sha256:'+'f'*64
    data['receipts'][1]=seal('receipt',data['receipts'][1],SigningKey(bytes(range(32,64))))
    with pytest.raises(SecurityException,match='broken-receipt-chain'):
        audit(data,trust)


def test_altered_decision_fails(bundle):
    data,trust=bundle
    next(iter(data['decisions'].values()))['verdict']='DENY'
    with pytest.raises(SecurityException,match='decision-hash-mismatch'):
        audit(data,trust)


def test_receipt_without_authorization_fails(bundle):
    data,trust=bundle
    data['authorizations'].clear()
    with pytest.raises(SecurityException,match='missing-authorization'):
        audit(data,trust)


def test_unsigned_authorization_fails(bundle):
    data,trust=bundle
    next(iter(data['authorizations'].values()))['gatekeeper_signature']='ed25519:'+'0'*128
    with pytest.raises(SecurityException,match='signature-invalid'):
        audit(data,trust)


@pytest.mark.parametrize('change',['prefix','suffix','empty','reorder'])
def test_missing_or_reordered_history_fails(bundle,change):
    data,trust=bundle
    if change=='prefix':data['receipts']=data['receipts'][1:]
    elif change=='suffix':data['receipts']=data['receipts'][:-1]
    elif change=='empty':data['receipts']=[]
    else:data['receipts'].reverse()
    with pytest.raises(SecurityException):
        audit(data,trust)


def test_receipt_replay_fails(bundle):
    data,trust=bundle
    data['receipts'].append(copy.deepcopy(data['receipts'][0]))
    with pytest.raises(SecurityException,match='chain-replay'):
        audit(data,trust)


def test_unknown_adapter_key_fails(bundle):
    data,trust=bundle
    trust['adapter_pubkeys']={}
    with pytest.raises(SecurityException,match='unknown-adapter-key'):
        audit(data,trust)


def test_genesis_state_is_checked(bundle):
    data,trust=bundle
    trust['genesis_state_hash']='sha256:'+'f'*64
    with pytest.raises(SecurityException,match='state-root-discontinuity'):
        audit(data,trust)
