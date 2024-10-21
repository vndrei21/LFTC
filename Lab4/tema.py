#re.findall(r'\w+|[^\s\w]'
import re
# Create a dictionary to hold the token mappings
atoms = {
    "ID": 0,
    "CONST": 1,
    "program": 2,
    "begin": 3,
    "var": 4,
    "type": 5,
    "end": 6,
    "integer": 7,
    "real": 8,
    "if": 9,
    "while": 10,
    "readln": 11,
    "writeln": 12,
    ".": 13,
    ",": 14,
    ";": 15,
    "+": 16,
    "-": 17,
    "*": 18,
    ":=": 19,
    "<": 20,
    ">": 21,
    "<>": 22,
    ":": 23,
    "(": 24,
    ")": 25
}

def convertelem(elem):
    if elem in atoms.keys():
        return atoms[elem]
    elif elem in [x for x in range(0,10)]:
        return atoms["CONST"]
    elif elem.isalpha() and len(elem) == 1:
        return atoms["ID"]
    return None

def createFirstTable(program):
    program = re.findall(r'\w+|[^\s\w]',program)
    print(program)
    tabel ={}
    for element in program:
        token = convertelem(element)
        if element is not None:
            tabel[element] = token
    return tabel


program = """
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
print(createFirstTable(program))



class Atom:
    def __init__(self,  value, tsvalue):
        self._type = type
        self._tsvalue = tsvalue
        self._value = value
    def get_value(self):
        return self._value

    def set_value(self, value):
        return self._value
    def set_tsvalue(self, tsvalue):
        self._tsvalue = tsvalue

    def get_tsvalue(self):
        return self._tsvalue
    def get_type(self):
        return self._type
    def set_type(self, type):
        self._type = type

    def __str__(self):
        return f'symbol: {self._type}, value: {self._value}'
class HashTable:
    def __init__(self, size):
        # Inițializează tabela de dispersie cu dimensiunea dată
        self.size = size
        self.table = [[] for _ in range(size)]  # Lista de liste (chaining)
    def hash_function(self, key):
        # Funcția de hash: folosește hash() și reduce valoarea la dimensiunea tabelei
        return hash(key) % self.size
    def add(self, key, value):
        # Calculează hash-ul și indicele pentru cheia dată
        index = self.hash_function(key)
        # Verifică dacă cheia există deja în tabelă, dacă da, actualizează valoarea
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        # Dacă cheia nu există, adaugă perechea (cheie, valoare) la lista de la indexul calculat
        self.table[index].append([key, value])
        print(f"Added: {key} -> {value}")
    def get(self, key):
        # Calculează hash-ul și găsește cheia
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]  # Returnează valoarea asociată cheii

        return None  # Cheia nu a fost găsită

    def __str__(self):
        # Format the hash table output with indexes and symbols
        table_str = "HashTable:\n"
        for i, bucket in enumerate(self.table):
            table_str += f"Index {i}: "
            if bucket:
                table_str += ", ".join([str(pair[1]) for pair in bucket]) + "\n"
            else:
                table_str += "Empty\n"
        return table_str


class Simbol:

    def __init__(self, symbol, info):
        self.symbol = symbol
        self.info = info

    def __str__(self):
        return f"simbol: {self.symbol}  info:{self.info}"

def create_ts(program):
    dict = createFirstTable(program)
    print(type(dict))
    table_id = HashTable(32)
    table_const = HashTable(10)
    id_key=0
    const_key = 0
    for key,val in dict.items():
        if val == 0:
            table_id.add(ord(key)-ord('a'),Simbol(key,None))
            id_key += 1
        elif val == 1:
            table_const.add(const_key,Simbol(key,None))
            const_key += 1
    print(id_key,const_key)
    write_to_file(table_id,"TS_id.txt")
    write_to_file(table_const,"Const_id.txt")
    write_FIP(dict,table_id,table_const)


def write_FIP(dict,table_id, table_const):
    with open("fip.txt","w") as file:
        for key,val in dict.items():
            if val == 0:
                file.write(f"atom {key} cod atom: {val} pozitie ts:{ord(key) - ord('a')}\n")
            elif val == 1:
                file.write(f"atom {key} cod atom: {val} pozitie ts: {table_const.hash_function(val)}\n")
            else:
                file.write(f"atom {key} cod atom: {val}\n")
def write_to_file(dict,file):
    with open(file, "w") as file:
        file.write(str(dict))
program = """
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
create_ts(program)
