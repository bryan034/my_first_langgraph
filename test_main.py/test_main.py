from main import decide 

def test_approve_bonundary_80():
    test_state = {
        "fit_score":80, 
        "status":"evaluated",
    }
    r = decide(test_state)
    assert r == 'approve'

def test_approve_bonundary_79():
        test_state = {
            "fit_score":79, 
            "status":"evaluated",
        }
        r = decide(test_state)
        assert r == 'review'

def test_approve_bonundary_50():
        test_state = {
            "fit_score":50, 
            "status":"evaluated",
        }
        r = decide(test_state)
        assert r == 'review'

def test_approve_bonundary_49():
        test_state = {
            "fit_score":49, 
            "status":"evaluated",
        }
        r = decide(test_state)
        assert r == 'reject'

def test_approve_bonundary_100():
        test_state = {
            "fit_score":100, 
            "status":"pending",
        }
        r = decide(test_state)
        assert r == 'error'


