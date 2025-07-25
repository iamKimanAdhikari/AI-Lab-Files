class FamilyTree:
    def __init__(self):
        self.facts = set()

    def add_fact(self, relation, person1, person2):
        relation = relation.strip().lower()
        person1 = person1.strip().lower()
        person2 = person2.strip().lower()

        if relation == 'child':
            relation = 'parent'
            person1, person2 = person2, person1

        if relation != 'parent':
            print("❌ Only 'parent' or 'child' relationships allowed.")
            return

        fact = (relation, person1, person2)
        if fact not in self.facts:
            self.facts.add(fact)
            print(f"✅ Added: {person1.capitalize()} is parent of {person2.capitalize()}")
        else:
            print(f"⚠️ Fact already exists.")

    def get_children(self, person):
        return {child for (rel, p, child) in self.facts if rel == 'parent' and p == person}

    def get_parents(self, person):
        return {p for (rel, p, c) in self.facts if rel == 'parent' and c == person}

    def is_sibling(self, person1, person2):
        if person1 == person2:
            return False
        parents1 = self.get_parents(person1)
        parents2 = self.get_parents(person2)
        return len(parents1 & parents2) > 0

    def get_siblings(self, person):
        all_people = self.get_all_people()
        return {p for p in all_people if self.is_sibling(person, p)}

    def is_grandparent(self, grandparent, person):
        parents = self.get_parents(person)
        for parent in parents:
            if grandparent in self.get_parents(parent):
                return True
        return False

    def get_grandchildren(self, person):
        children = self.get_children(person)
        grandchildren = set()
        for child in children:
            grandchildren |= self.get_children(child)
        return grandchildren

    def is_uncle_or_aunt(self, uncle_or_aunt, person):
        parents = self.get_parents(person)
        for parent in parents:
            if self.is_sibling(uncle_or_aunt, parent):
                return True
        return False

    def get_all_people(self):
        people = set()
        for (_, p1, p2) in self.facts:
            people.add(p1)
            people.add(p2)
        return people

    def query(self, relation, person1, person2=None):
        person1 = person1.strip().lower()
        if person2:
            person2 = person2.strip().lower()

        if relation == 'parent':
            result = person2 in self.get_children(person1)
        elif relation == 'child':
            result = person2 in self.get_parents(person1)
        elif relation == 'sibling':
            result = self.is_sibling(person1, person2)
        elif relation == 'grandparent':
            result = self.is_grandparent(person1, person2)
        elif relation == 'grandchild':
            result = self.is_grandparent(person2, person1)
        elif relation == 'uncle_or_aunt':
            result = self.is_uncle_or_aunt(person1, person2)
        elif relation == 'nephew_or_niece':
            result = self.is_uncle_or_aunt(person2, person1)
        else:
            print("❌ Unknown relation.")
            return False

        print(f"Query: Is {person1.capitalize()} {relation.replace('_', ' ')} of {person2.capitalize()}?")
        print(f"Answer: {'✅ Yes' if result else '❌ No'}")
        return result

    def list_relation(self, relation, person):
        person = person.strip().lower()
        if relation == 'parent':
            result = self.get_parents(person)
        elif relation == 'child':
            result = self.get_children(person)
        elif relation == 'sibling':
            result = self.get_siblings(person)
        elif relation == 'grandparent':
            result = {gp for gp in self.get_all_people() if self.is_grandparent(gp, person)}
        elif relation == 'grandchild':
            result = self.get_grandchildren(person)
        elif relation == 'uncle_or_aunt':
            result = {ua for ua in self.get_all_people() if self.is_uncle_or_aunt(ua, person)}
        elif relation == 'nephew_or_niece':
            result = {n for n in self.get_all_people() if self.is_uncle_or_aunt(person, n)}
        else:
            print("❌ Unknown relation.")
            return

        formatted = ', '.join(sorted(p.capitalize() for p in result)) if result else "None"
        print(f"{relation.replace('_', ' ').capitalize()}(s) of {person.capitalize()}: {formatted}")


    def print_all_facts(self):
        print("\n📚 Known Facts:")
        for (rel, p1, p2) in sorted(self.facts):
            print(f"  {p1.capitalize()} is {rel} of {p2.capitalize()}")

def run_family_tree():
    ft = FamilyTree()

    print("👨‍👩‍👧 Family Tree Inference System")
    print("Type 'help' for available commands.")

    while True:
        command = input("\n>>> ").strip().lower()

        if command == 'exit':
            print("👋 Exiting.")
            break

        elif command == 'help':
            print("""
Available commands:
  add parent [A] [B]     → A is parent of B
  add child [A] [B]      → A is child of B
  query [rel] [A] [B]    → Is A [rel] of B?
  list [rel] [A]         → List all [rel]s of A
  show                   → Show all known facts
  exit                   → Quit the program

Valid relations:
  parent, child, sibling, grandparent, grandchild, uncle_or_aunt, nephew_or_niece
""")

        elif command.startswith('add'):
            parts = command.split()
            if len(parts) != 4:
                print("⚠️ Usage: add parent/child person1 person2")
                continue
            _, rel, p1, p2 = parts
            ft.add_fact(rel, p1, p2)

        elif command.startswith('query'):
            parts = command.split()
            if len(parts) != 4:
                print("⚠️ Usage: query relation person1 person2")
                continue
            _, rel, p1, p2 = parts
            ft.query(rel, p1, p2)

        elif command.startswith('list'):
            parts = command.split()
            if len(parts) != 3:
                print("⚠️ Usage: list relation person")
                continue
            _, rel, p = parts
            ft.list_relation(rel, p)

        elif command == 'show':
            ft.print_all_facts()

        else:
            print("❓ Unknown command. Type 'help' for options.")


def main():
    run_family_tree()

if __name__ == "__main__":
    main()