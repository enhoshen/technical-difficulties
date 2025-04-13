# Troubleshooting with tests

<!--toc:start-->

- [Troubleshooting with tests](#troubleshooting-with-tests)
  - [Different test orders produces different result](#different-test-orders-produces-different-result) - [Causes](#causes) - [What to do:](#what-to-do)
  <!--toc:end-->

## Different test orders produces different result

### Causes

- Global module/class/state changing side effects:  
  Even if testing framework does clean up for us, if some tests mess
  up module, class or global states, and they are used in the subsequent
  tests, then following tests may pass on their own, but not preceded by
  the state changing tests.

### What to do:

- Pinpoint the location of the side effect by running specific tests to limit
  exploration scope
  EX: from `pytest A/ B/` to
  `pytest A/test_a.py::TestA::test_side_effect_candidate B/test_b.py::TestB::test_that_passes_alone`
  ,maybe writing a script or using test framework feature to sweep through
  side effect candidates along with the test that run fine on its own.
