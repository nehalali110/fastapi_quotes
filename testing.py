import re

email_sample = "abc@xyz."
pattern_search = re.search(r"\w+\@\w+\.\w{2,3}+", email_sample)
print(pattern_search)