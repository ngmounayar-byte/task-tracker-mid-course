# Verification

## Backend test results

Command used after restoring the correct implementation:

```bash
pytest -q
```

Actual pytest output:

```text
.................                                                        [100%]
17 passed in 0.27s
```

The automated tests cover due dates, overdue filtering, tag validation and filtering, partial-update preservation, explicit-null rejection, and omitted-field behavior.

## Break Test evidence

The purpose of this break test was to prove that the automated test suite detects a real regression and that the test passes again after the implementation is fixed.

### Test selected

```text
test_done_task_is_not_overdue
```

### Correct behavior

A task whose due date is in the past must **not** be reported as overdue when its status is `done`.

The correct implementation in `Task.overdue` is:

```python
return self.due_date is not None and self.due_date < date.today() and self.status != Status.done
```

### Step 1 — intentionally introduce a regression

For the break test only, I temporarily changed the implementation to:

```python
return self.due_date is not None and self.due_date < date.today()
```

This intentionally removes the `self.status != Status.done` protection.

Command executed:

```bash
pytest -q tests/test_tasks.py::test_done_task_is_not_overdue
```

Actual failing pytest output:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
________________________ test_done_task_is_not_overdue _________________________

    def test_done_task_is_not_overdue(client):
        make_task(client,title='Completed late task',due_date=(date.today()-timedelta(days=1)).isoformat(),status='done')
>       response=client.get('/tasks',params={'overdue':'true'}); assert response.status_code==200; assert response.json()==[]
E       AssertionError: assert [{'assignee':...'id': 1, ...}] == []
E       Left contains one more item: {'assignee': 'Nathalie', 'description': 'A test task', 'due_date': '2026-08-15', 'id': 1, ...}

FAILED tests/test_tasks.py::test_done_task_is_not_overdue - AssertionError
1 failed in 0.25s
```

This failure proves that the test catches the regression: a completed task incorrectly appears in the overdue results.

### Step 2 — restore the fix

I restored the original correct condition:

```python
return self.due_date is not None and self.due_date < date.today() and self.status != Status.done
```

Then I executed the complete test suite again:

```bash
pytest -q
```

Actual passing pytest output:

```text
.................                                                        [100%]
17 passed in 0.27s
```

Therefore, the break-test sequence is demonstrated with both real failing pytest output and real passing pytest output after the fix.

## Reviewer corrections

- Explicit `null` values for `title`, `status`, `priority`, and `tags` return HTTP 422.
- Partial PATCH updates preserve omitted fields because `payload.model_dump(exclude_unset=True)` is used.
- Completed past-due tasks are excluded from overdue results.
- Automated tests verify the corrected behavior.

## Repository cleanup required before resubmission

The valid pytest suite is `tests/test_tasks.py`. A separate root-level `test_tasks.py` currently contains CSS rather than Python and should be removed so that pytest does not try to collect an invalid test module.

The existing root `TEST-RESULTS.txt` should also be replaced with the actual passing pytest output supplied with this resubmission.
