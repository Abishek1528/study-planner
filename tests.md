# StudyMate - Test Scenarios

## Test 1: Memory Test

**Input:** `My exam subject is Biology.`
**Follow-up:** `Which is my exam subject?`

**Expected Result:** The assistant remembers Biology.

**Status:** Requires a live Gemini API key.

## Test 2: Days Until Exam Tool

**Input:** `My exam is on a future date. How many days are left?`

**Expected Result:** The assistant uses `days_until_exam()` and calculates the
remaining days accurately.

**Automated check:** `test_days_until_exam()` passes in `test_tools.py`.

**Status:** Pass (deterministic tool behavior)

## Test 3: Study Hours Tool

**Input:** `Divide 6 hours among Maths, Physics and Chemistry.`

**Expected Result:** The assistant divides 2 hours to each subject.

**Automated check:** `test_split_study_hours()` passes in `test_tools.py`.

**Status:** Pass (deterministic tool behavior)

## Test 4: Normal Question

**Input:** `Give me three tips to avoid distractions.`

**Expected Result:** The assistant gives useful study tips without using a tool.

**Status:** Requires a live Gemini API key.

## Test 5: Outside Topic

**Input:** `Tell me the latest cricket score.`

**Expected Result:** The assistant politely explains that cricket scores are
outside its study-planning purpose.

**Status:** Requires a live Gemini API key.

## Test 6: Invalid Input

**Input:** `My exam is next Friday. How many days are left?`

**Expected Result:** The assistant asks for a date in `YYYY-MM-DD` format.

**Automated check:** `test_invalid_exam_date()` passes in `test_tools.py`.

**Status:** Pass (deterministic tool behavior)
