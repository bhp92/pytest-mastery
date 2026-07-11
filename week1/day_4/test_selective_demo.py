import pytest
from source import add, divide, slow_batch_process

# ── Markers used below must be registered in pytest.ini ────────
# (yours already has: slow, integration, unit)

@pytest.mark.unit
def test_add_positive_numbers():
    assert add(2, 3) == 5

@pytest.mark.unit
def test_add_negative_numbers():
    assert add(-2, -3) == -5

@pytest.mark.unit
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.mark.slow
def test_slow_batch_process():
    # print only shows up if you run with -s
    print("Running the slow batch job...")
    result = slow_batch_process([1, 2, 3, 4, 5])
    assert result == 10

@pytest.mark.integration
def test_divide_realistic_case():
    assert divide(10, 5) == 2.0

# ── TRY THESE FROM THE week1/day4 DIRECTORY ────────────────────
#
# Run only unit tests:
#   pytest -m "unit" -v
# 
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -m "unit" -v
# =================================================================================================== test session starts ===================================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=1261434367
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items / 2 deselected / 3 selected
#
# test_selective_demo.py::test_add_negative_numbers PASSED                                                                                                                                                            [ 33%]
# test_selective_demo.py::test_divide_by_zero_raises PASSED                                                                                                                                                           [ 66%]
# test_selective_demo.py::test_add_positive_numbers PASSED                                                                                                                                                            [100%]
#
# ============================================================================================= 3 passed, 2 deselected in 0.01s =============================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# Run everything except slow tests:
#   pytest -m "not slow" -v
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -m "not slow" -v
# =================================================================================================== test session starts ===================================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=3681215507
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items / 1 deselected / 4 selected
#
# test_selective_demo.py::test_add_negative_numbers PASSED                                                                                                                                                            [ 25%]
# test_selective_demo.py::test_divide_realistic_case PASSED                                                                                                                                                           [ 50%]
# test_selective_demo.py::test_divide_by_zero_raises PASSED                                                                                                                                                           [ 75%]
# test_selective_demo.py::test_add_positive_numbers PASSED                                                                                                                                                            [100%]
#
# ============================================================================================= 4 passed, 1 deselected in 0.01s =============================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# Run only tests with "divide" in the name:
#   pytest -k "divide" -v
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -k "divide" -v
# =================================================================================================== test session starts ===================================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=4097643379
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items / 3 deselected / 2 selected
#
# test_selective_demo.py::test_divide_by_zero_raises PASSED                                                                                                                                                           [ 50%]
# test_selective_demo.py::test_divide_realistic_case PASSED                                                                                                                                                           [100%]
#
# ============================================================================================= 2 passed, 3 deselected in 0.01s =============================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# Run tests matching name AND not slow:
#   pytest -k "add and not negative" -v
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -k "add and not negative" -v
# =================================================================================================== test session starts ===================================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=3805755416
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items / 4 deselected / 1 selected
#
# test_selective_demo.py::test_add_positive_numbers PASSED                                                                                                                                                            [100%]
#
# ============================================================================================= 1 passed, 4 deselected in 0.01s =============================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# Stop after the first failure:
#   pytest -x
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -x
# ========================================================================================== test session starts ==========================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=760833894
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items
#
# test_selective_demo.py::test_divide_realistic_case PASSED                                                                                                                                          [ 20%]
# test_selective_demo.py::test_divide_by_zero_raises PASSED                                                                                                                                          [ 40%]
# test_selective_demo.py::test_add_positive_numbers PASSED                                                                                                                                           [ 60%]
# test_selective_demo.py::test_slow_batch_process FAILED                                                                                                                                             [ 80%]
#
# ================================================================================================ FAILURES ===============================================================================================
# ________________________________________________________________________________________ test_slow_batch_process ________________________________________________________________________________________
# test_selective_demo.py:25: in test_slow_batch_process
#     assert result == 10
# E   assert 15 == 10
# ------------------------------------------------------------------------------------------ Captured stdout call -----------------------------------------------------------------------------------------
# Running the slow batch job...
# ======================================================================================== short test summary info ========================================================================================
# FAILED test_selective_demo.py::test_slow_batch_process - assert 15 == 10
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ====================================================================================== 1 failed, 3 passed in 0.36s ======================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -x
# ========================================================================================== test session starts ==========================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=126565608
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items
#
# test_selective_demo.py::test_add_negative_numbers PASSED                                                                                                                                           [ 20%]
# test_selective_demo.py::test_divide_realistic_case PASSED                                                                                                                                          [ 40%]
# test_selective_demo.py::test_slow_batch_process FAILED                                                                                                                                             [ 60%]
#
# ================================================================================================ FAILURES ===============================================================================================
# ________________________________________________________________________________________ test_slow_batch_process ________________________________________________________________________________________
# test_selective_demo.py:25: in test_slow_batch_process
#     assert result == 10
# E   assert 15 == 10
# ------------------------------------------------------------------------------------------ Captured stdout call -----------------------------------------------------------------------------------------
# Running the slow batch job...
# ======================================================================================== short test summary info ========================================================================================
# FAILED test_selective_demo.py::test_slow_batch_process - assert 15 == 10
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ====================================================================================== 1 failed, 2 passed in 0.36s ======================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -p no:randomly -x
# ========================================================================================== test session starts ==========================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items
#
# test_selective_demo.py::test_add_positive_numbers PASSED                                                                                                                                           [ 20%]
# test_selective_demo.py::test_add_negative_numbers PASSED                                                                                                                                           [ 40%]
# test_selective_demo.py::test_divide_by_zero_raises PASSED                                                                                                                                          [ 60%]
# test_selective_demo.py::test_slow_batch_process FAILED                                                                                                                                             [ 80%]
#
# ================================================================================================ FAILURES ===============================================================================================
# ________________________________________________________________________________________ test_slow_batch_process ________________________________________________________________________________________
# test_selective_demo.py:25: in test_slow_batch_process
#     assert result == 10
# E   assert 15 == 10
# ------------------------------------------------------------------------------------------ Captured stdout call -----------------------------------------------------------------------------------------
# Running the slow batch job...
# ======================================================================================== short test summary info ========================================================================================
# FAILED test_selective_demo.py::test_slow_batch_process - assert 15 == 10
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ====================================================================================== 1 failed, 3 passed in 0.37s ======================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# NOTE:
# The change in test execution order is NOT caused by the `-x` flag.
# It is caused by the `pytest-randomly` plugin (visible in the plugin list).
# Each test run uses a different random seed (e.g., "Using --randomly-seed=3805755416"),
# which shuffles the test execution order to detect hidden dependencies between tests.
#
# `-x` simply stops the test run after the first failure; it never changes the order.
#
# To disable random ordering temporarily:
#     pytest -p no:randomly -v
# or
#     pytest -p no:randomly -x -v
#
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# See print() output from the slow test:
#   pytest -m "slow" -s -v
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest -m "slow" -s -v
# =================================================================================================== test session starts ===================================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=428330582
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items / 4 deselected / 1 selected
#
# test_selective_demo.py::test_slow_batch_process Running the slow batch job...
# FAILED
#
# ======================================================================================================== FAILURES =========================================================================================================
# _________________________________________________________________________________________________ test_slow_batch_process _________________________________________________________________________________________________
# test_selective_demo.py:25: in test_slow_batch_process
#     assert result == 10
# E   assert 15 == 10
# ================================================================================================= short test summary info =================================================================================================
# FAILED test_selective_demo.py::test_slow_batch_process - assert 15 == 10
# ============================================================================================= 1 failed, 4 deselected in 0.36s =============================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
#
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# Minimal traceback on failure (good for quick CI logs):
#   pytest --tb=short
#
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$ pytest --tb=short
# =================================================================================================== test session starts ===================================================================================================
# platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /home/bpuranik/pytest-mastery/.venv/bin/python3
# cachedir: .pytest_cache
# benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
# Using --randomly-seed=1700922771
# rootdir: /home/bpuranik/pytest-mastery
# configfile: pytest.ini
# plugins: repeat-0.9.4, asyncio-1.4.0, anyio-4.13.0, mock-3.15.1, xdist-3.8.0, benchmark-5.2.3, randomly-4.1.0, cov-7.1.0
# asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collected 5 items
#
# test_selective_demo.py::test_add_positive_numbers PASSED                                                                                                                                                            [ 20%]
# test_selective_demo.py::test_slow_batch_process FAILED                                                                                                                                                              [ 40%]
# test_selective_demo.py::test_divide_realistic_case PASSED                                                                                                                                                           [ 60%]
# test_selective_demo.py::test_divide_by_zero_raises PASSED                                                                                                                                                           [ 80%]
# test_selective_demo.py::test_add_negative_numbers PASSED                                                                                                                                                            [100%]
#
# ======================================================================================================== FAILURES =========================================================================================================
# _________________________________________________________________________________________________ test_slow_batch_process _________________________________________________________________________________________________
# test_selective_demo.py:25: in test_slow_batch_process
#     assert result == 10
# E   assert 15 == 10
# -------------------------------------------------------------------------------------------------- Captured stdout call ---------------------------------------------------------------------------------------------------
# Running the slow batch job...
# ================================================================================================= short test summary info =================================================================================================
# FAILED test_selective_demo.py::test_slow_batch_process - assert 15 == 10
# =============================================================================================== 1 failed, 4 passed in 0.38s ===============================================================================================
# (.venv) bpuranik@lab:~/pytest-mastery/week1/day_4$
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────