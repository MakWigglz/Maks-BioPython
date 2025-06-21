import numpy as np
from typing import TypeVar, Optional, Union # Use Union for | in Python < 3.10

# Define a placeholder for Residue, as Atom.parent uses it
class Residue:
    """Placeholder for the Residue class that an Atom might belong to."""
    def __init__(self, name: str, res_id: int):
        self.name = name
        self.id = res_id
        self.atoms = [] # List to hold Atom objects


_AtomT = TypeVar("_AtomT", bound="Atom")

class Atom:
    """Define Atom class.

    The Atom object stores atom name (both with and without spaces),
    coordinates, B factor, occupancy, alternative location specifier
    and (optionally) anisotropic B factor and standard deviations of
    B factor and positions.

    In the case of PQR files, B factor and occupancy are replaced by
    atomic charge and radius.
    """

    def __init__(
        self,
        name: str,
        coord: np.ndarray,
        bfactor: float | None,
        occupancy: float | None,
        altloc: str,
        fullname: str,
        serial_number: int, # Explicitly typed as int for clarity, common for PDB serials
        element: str | None = None,
        pqr_charge: float | None = None,
        radius: float | None = None,
    ):
        """Initialize Atom object.

        :param name: atom name (eg. "CA"). Note that spaces are normally stripped.
        :type name: string

        :param coord: atomic coordinates (x,y,z)
        :type coord: NumPy array (Float0, length 3)

        :param bfactor: isotropic B factor
        :type bfactor: number

        :param occupancy: occupancy (0.0-1.0)
        :type occupancy: number

        :param altloc: alternative location specifier for disordered atoms
        :type altloc: string

        :param fullname: full atom name, including spaces, e.g. " CA ". Normally
                         these spaces are stripped from the atom name.
        :type fullname: string

        :param element: atom element, e.g. "C" for Carbon, "HG" for mercury,
        :type element: uppercase string (or None if unknown)

        :param pqr_charge: atom charge
        :type pqr_charge: number

        :param radius: atom radius
        :type radius: number
        """
        self.level = "A"
        # Reference to the residue
        self.parent: Residue | None = None # Correctly typed now with the placeholder
        # the atomic data
        self.name = name  # eg. CA, spaces are removed from atom name
        self.fullname = fullname  # e.g. " CA ", spaces included
        self.coord = coord
        self.bfactor = bfactor
        self.occupancy = occupancy
        self.altloc = altloc
        self.full_id = None  # (structure id, model id, chain id, residue id, atom id)
        self.id = name  # id of atom is the atom name (e.g. "CA")
        self.disordered_flag = 0
        self.anisou_array = None
        self.siguij_array = None
        self.sigatm_array = None
        self.serial_number = serial_number
        # Dictionary that keeps additional properties
        self.xtra: dict = {}
        assert not element or element == element.upper(), element
        self.element = self._assign_element(element) # Placeholder for this method
        self.mass = self._assign_atom_mass()       # Placeholder for this method
        self.pqr_charge = pqr_charge
        self.radius = radius

        # For atom sorting (protein backbone atoms first)
        self._sorting_keys = {"N": 0, "CA": 1, "C": 2, "O": 3}

    # --- Placeholder methods that Atom.__init__ calls ---
    def _assign_element(self, element: Optional[str]) -> Optional[str]:
        """A placeholder for actual element assignment logic.
        In a real scenario, this might standardize element names or look them up."""
        return element

    def _assign_atom_mass(self) -> Optional[float]:
        """A placeholder for actual atomic mass lookup.
        In a real scenario, this would use self.element to find the mass."""
        if self.element == "C":
            return 12.011 # Carbon mass
        elif self.element == "O":
            return 15.999 # Oxygen mass
        elif self.element == "N":
            return 14.007 # Nitrogen mass
        # Add more elements as needed
        return None # Return None if element is unknown or not handled

    # You might want a __repr__ for easy printing of Atom objects
    def __repr__(self) -> str:
        return (
            f"Atom(name='{self.name}', coord={self.coord.tolist()}, "
            f"bfactor={self.bfactor}, occupancy={self.occupancy}, "
            f"altloc='{self.altloc}', serial_number={self.serial_number}, "
            f"element='{self.element}', pqr_charge={self.pqr_charge}, radius={self.radius})"
        )


# --- Let's get an instance of the Atom object ---

# Example data for a Carbon Alpha (CA) atom in a protein backbone
# You need to provide valid data for all arguments in the __init__ method.
ca_atom_instance = Atom(
    name="CA",
    coord=np.array([15.234, 12.567, 8.901]),  # Example coordinates
    bfactor=35.7,                           # Example B-factor
    occupancy=1.0,                          # Full occupancy
    altloc=" ",                             # No alternative location
    fullname=" CA ",                        # Full name with spaces
    serial_number=25,                       # Serial number
    element="C",                            # Element symbol
    pqr_charge=None,                        # Not a PQR file, so no charge/radius
    radius=None,
)

print("Successfully instantiated an Atom object:")
print(ca_atom_instance)

# You can also access its attributes:
print(f"\nAtom Name: {ca_atom_instance.name}")
print(f"Atom Full Name: '{ca_atom_instance.fullname}'")
print(f"Coordinates: {ca_atom_instance.coord}")
print(f"B-factor: {ca_atom_instance.bfactor}")
print(f"Occupancy: {ca_atom_instance.occupancy}")
print(f"Alternative Location: '{ca_atom_instance.altloc}'")
print(f"Serial Number: {ca_atom_instance.serial_number}")
print(f"Element: {ca_atom_instance.element}")
print(f"Mass: {ca_atom_instance.mass}")
print(f"PQR Charge: {ca_atom_instance.pqr_charge}")
print(f"Radius: {ca_atom_instance.radius}")

# Example of an atom with alternative location and partial occupancy
o_atom_altB = Atom(
    name="O",
    coord=np.array([16.123, 11.987, 9.543]),
    bfactor=45.1,
    occupancy=0.5,
    altloc="B",
    fullname=" O  ",
    serial_number=26,
    element="O",
)

print("\nSuccessfully instantiated another Atom object (with alternative location):")
print(o_atom_altB)
print(f"Atom Name: {o_atom_altB.name}")
print(f"Alternative Location: '{o_atom_altB.altloc}'")
print(f"Occupancy: {o_atom_altB.occupancy}")
print(f"Mass: {o_atom_altB.mass}")

# Example of an atom from a PQR file (charge and radius instead of bfactor/occupancy)
h_atom_pqr = Atom(
    name="H1",
    coord=np.array([10.0, 10.0, 10.0]),
    bfactor=None,      # Not used in PQR
    occupancy=None,    # Not used in PQR
    altloc=" ",
    fullname=" H1 ",
    serial_number=1,
    element="H",
    pqr_charge=0.25,   # PQR charge
    radius=1.2,        # PQR radius
)

print("\nSuccessfully instantiated an Atom object (PQR style):")
print(h_atom_pqr)
print(f"PQR Charge: {h_atom_pqr.pqr_charge}")
print(f"Radius: {h_atom_pqr.radius}")

Successfully instantiated an Atom object:
Atom(name='CA', coord=[15.234, 12.567, 8.901], bfactor=35.7, occupancy=1.0, altloc=' ', serial_number=25, element='C', pqr_charge=None, radius=None)

Atom Name: CA
Atom Full Name: ' CA '
Coordinates: [15.234 12.567  8.901]
B-factor: 35.7
Occupancy: 1.0
Alternative Location: ' '
Serial Number: 25
Element: C
Mass: 12.011
PQR Charge: None
Radius: None

Successfully instantiated another Atom object (with alternative location):
Atom(name='O', coord=[16.123, 11.987, 9.543], bfactor=45.1, occupancy=0.5, altloc='B', serial_number=26, element='O', pqr_charge=None, radius=None)
Atom Name: O
Alternative Location: 'B'
Occupancy: 0.5
Mass: 15.999

Successfully instantiated an Atom object (PQR style):
Atom(name='H1', coord=[10.0, 10.0, 10.0], bfactor=None, occupancy=None, altloc=' ', serial_number=1, element='H', pqr_charge=0.25, radius=1.2)
PQR Charge: 0.25
Radius: 1.2
