import re

program="""
    var a,b; integer
    begin
        readln(a);
        readln(b);
        while b <> 0 do
        begin
            r := a % b;
            a := b;
            b := r;
        end
    writln(a);
    end.
"""
print(re.findall(r'\w+|[^\s\w]', program))
