import re
from flask import Markup
text = "haha baba"
print(re.sub('bab', Markup('<strong>lala</strong>'), text))
