import sys
import io

def run_tests(code, test_cases):
    results = []
    for test in test_cases:
        exec_code = f"{code}\nprint(second_largest({test['input']}))"
        stdout = io.StringIO()
        sys.stdout = stdout
        try:
            exec(exec_code, {})
            actual = stdout.getvalue().strip()
            passed = (actual == test['expected'])
            results.append({"passed": passed})
        except Exception as e:
            results.append({"passed": False})
        finally:
            sys.stdout = sys.__stdout__
    return results