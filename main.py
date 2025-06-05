#!/usr/bin/env python3
import argparse, requests
from progressbar import progressbar

# Arguments
parser = argparse.ArgumentParser(
    "grunt",
    description="A brute-force algorithm to potentially advance the Trench Crusade ARG.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-c", "--crumb",
    help="ID which is used to differentiate between valid sessions.",
    type=str
)

parser.add_argument(
    "-t", "--test",
    help="File which contains potential passwords",
    type=str,
    default="test.txt",
    nargs='?'
)

parser.add_argument(
    "-td", "--tested",
    help="File to which store all tested passwords in.",
    type=str,
    default="tested.txt",
    nargs='?'
)

parser.add_argument(
    "-g", "--generate",
    help="Whether or not to generate passwords before testing.",
    default=True,
    action="store_true"
)

args = parser.parse_args()

s = requests.session()
s.get("https://www.trenchcrusade.com/6d6574616d6f7270686973", headers={"DNT": "1", "Sec-GPC": "1", "Priority": "u=0, i"}, cookies={"crumb": args.crumb})
final_password = ""
testing_string = "===TESTING==="
done_string = "===DONE==="

def generate() -> list[str]:
    return ["example1", "example2", "example3"]

def test() -> str:
    testfile_content = []
    with open(args.test, "r", encoding="utf8") as test_file:
        testfile_content = test_file.read().splitlines()
    
    for i in progressbar(range(len(testfile_content))):
        line_array = testfile_content[i].split(' ')
        for line_entry in line_array:
            if line_entry and len(line_entry) < 31 and len(line_entry) > 3 and line_entry.strip():
                with open(args.tested, "r", encoding="utf8") as tested_file:
                    if line_entry.lower() in tested_file.read():
                        continue
                
                r1 = s.post("https://www.trenchcrusade.com/api/auth/visitor/collection", params={"crumb": args.crumb}, json={"password":line_entry.lower(),"collectionId":"680897a38eba8b1b034f8e1d"}, cookies={"crumb": args.crumb})
                while r1.status_code == 429: # too many requests
                    r1 = s.post("https://www.trenchcrusade.com/api/auth/visitor/collection", params={"crumb": args.crumb}, json={"password":line_entry.lower(),"collectionId":"680897a38eba8b1b034f8e1d"}, cookies={"crumb": args.crumb})

                
                r2 = s.post("https://www.trenchcrusade.com/api/auth/visitor/collection", params={"crumb": args.crumb}, json={"password":line_entry.capitalize(),"collectionId":"680897a38eba8b1b034f8e1d"}, cookies={"crumb": args.crumb})
                while r2.status_code == 429: # too many requests
                    r2 = s.post("https://www.trenchcrusade.com/api/auth/visitor/collection", params={"crumb": args.crumb}, json={"password":line_entry.capitalize(),"collectionId":"680897a38eba8b1b034f8e1d"}, cookies={"crumb": args.crumb})

                if r1.status_code > 199 and r1.status_code < 300:
                    return line_entry.lower()

                if r2.status_code > 199 and r2.status_code < 300:
                    return line_entry.capitalize()
                
                with open(args.tested, "a", encoding="utf8") as tested_file:           
                    tested_file.writelines(line_entry.lower())
    return ""

def done() -> None:
    if final_password:
        print("Password was found: '" + final_password + "'")
    else:
        print("No valid password was found.")


if __name__ == "__main__":
    if args.generate:
        generated_passwords = generate()
        saved_passwords = []
        with open(args.test, "r", encoding="utf8") as test_file:
            saved_passwords = test_file.read().splitlines()
        unique_passwords = list(set(saved_passwords + generated_passwords))
        print(generated_passwords)
        print(saved_passwords)
        print(unique_passwords)
        with open(args.test, "w", encoding="utf8") as test_file:
            test_file.write('\n'.join([x.strip() for x in unique_passwords if x.strip()]) + '\n')
    
    print(testing_string)
    final_password = test()
    print(testing_string)

    print(done_string)
    done()
    print(done_string)
