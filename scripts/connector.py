import numpy as np

class Connector(object):

    def bond_labels(self,atom_labels,bonds,bond_types):
        bond_labels = []
        for bond in bonds:
            atoms = [atom_labels[bond[0]-1],
                     atom_labels[bond[1]-1]]
            found = False
            for i in range(len(bond_types)):
                flag1 = bond_types[i]==atoms
                flag2 = bond_types[i]==list(reversed(atoms)) 
                if flag1 or flag2: 
                    bond_labels.append(i+1)
                    found = True
            if not found:
                raise TypeError('bond not found',atoms)
        if len(bond_labels) != len(bonds):
            raise ValueError('bond assignment went wrong')
        return bond_labels

    def angles(self,bonds):
        angles = np.empty((0,3),dtype=int)
        N = int(np.amax(bonds)) # Number of atoms
        
        for centre in range(1,N+1):
            neighbours = self.find_neighbours(bonds,centre)
            for i in range(len(neighbours)):
                for j in range(i+1,len(neighbours)):
                    angle = [neighbours[i],centre,neighbours[j]]
                    angles = np.vstack((angles,angle))
        return angles
    
    def angle_labels(self,atom_labels,angles,angle_types):
        angle_labels = []
        for angle in angles:
            atoms = [atom_labels[angle[0]-1],
                     atom_labels[angle[1]-1],
                     atom_labels[angle[2]-1]]
            found = False
            for i in range(len(angle_types)):
                flag1 = angle_types[i]==atoms
                flag2 = angle_types[i]==list(reversed(atoms))
                if flag1 or flag2: 
                    angle_labels.append(i+1)
                    found = True
            if not found:
                raise TypeError('angle not found',atoms)
        if len(angle_labels) != len(angles):
            raise ValueError('angle assignment went wrong')
        return angle_labels

    def dihedrals(self,bonds):
        dihedrals = np.empty((0,4),dtype=int)
        for bond in bonds:
            neighbours1 = self.find_neighbours(bonds,bond[0])
            neighbours1.remove(bond[1])
            neighbours2 = self.find_neighbours(bonds,bond[1])
            neighbours2.remove(bond[0])
            if len(neighbours1) and len(neighbours2):
                for neighbour1 in neighbours1:
                    for neighbour2 in neighbours2:
                        dihedral = [neighbour1,bond[0],
                                   bond[1],neighbour2]
                        dihedrals = np.vstack((dihedrals,dihedral))
        return dihedrals       

    def dihedral_labels(self,atom_labels,dihedrals,dihedral_types):
        dihedral_labels = []
        for dihedral in dihedrals:
            atoms = [atom_labels[dihedral[0]-1],
                     atom_labels[dihedral[1]-1],
                     atom_labels[dihedral[2]-1],
                     atom_labels[dihedral[3]-1]]
            found = False
            for i in range(len(dihedral_types)):
                flag1 = dihedral_types[i]==atoms
                flag2 = dihedral_types[i]==list(reversed(atoms))
                if flag1 or flag2: 
                    dihedral_labels.append(i+1)
                    found = True
            if not found:
#                dihedral_types += [atoms]
                raise TypeError('dihedral not found',atoms)
        if len(dihedral_labels) != len(dihedrals):
            raise ValueError('dihedral assignment went wrong')
#        print 'types ',len(dihedral_types)
#        print dihedral_types
        return dihedral_labels

    def impropers(self,bonds):
        impropers = np.empty((0,4),dtype=int)
        N = int(np.amax(bonds)) # Number of atoms
        for centre in range(1,N+1):
            neighbours = self.find_neighbours(bonds,centre)
            if len(neighbours) == 3:
                improper = [centre,neighbours[0],
                            neighbours[1],neighbours[2]]
                impropers = np.vstack((impropers,improper))
        return impropers
    
    def improper_labels(self,atom_labels, impropers,improper_types):
        improper_labels = []
        for improper in impropers:
            atoms = [atom_labels[improper[0]-1],
                     atom_labels[improper[1]-1],
                     atom_labels[improper[2]-1],
                     atom_labels[improper[3]-1]]
            for i in range(len(improper_types)):
                flag1 = improper_types[i][0]==atoms[0]
                flag2 = set(improper_types[i][1:])==set(atoms[1:]) 
                if flag1 and flag2:
                    improper_labels.append(i+1)
            #print atoms
        if len(improper_labels) != len(impropers):
            print len(improper_labels), len(impropers)
            raise ValueError('improper assignment went wrong',len(improper_labels))
        return improper_labels

    def find_connections(self,bonds,centre):
        connections = np.where(bonds==centre)
        connections =np.vstack((connections[0],connections[1]))
        return connections.transpose()
            
    def find_neighbours(self,bonds,centre):
        connections = self.find_connections(bonds,centre)
        neighbours = []
        for connection in connections:
            # Find atom connected to centre
            neighbour = bonds[connection[0]][connection[1]-1]
            neighbours.append(neighbour)
        return neighbours

    def find_dihedral_types(self,atom_labels,dihedrals):
        dihedral_types = []
        for dihedral in dihedrals:
            atoms = [atom_labels[dihedral[0]-1],
                     atom_labels[dihedral[1]-1],
                     atom_labels[dihedral[2]-1],
                     atom_labels[dihedral[3]-1]]
            found = False
            for i in range(len(dihedral_types)):
                flag1 = dihedral_types[i]==atoms
                flag2 = dihedral_types[i]==list(reversed(atoms))
                if flag1 or flag2: 
                    found = True
            if not found:
                dihedral_types += [atoms]
        return dihedral_types

    def find_bond_types(self,atom_labels,bonds):
        bond_types = []
        for bond in bonds:
            atoms = [atom_labels[bond[0]-1],
                     atom_labels[bond[1]-1]]
            found = False
            for i in range(len(bond_types)):
                flag1 = bond_types[i]==atoms
                flag2 = bond_types[i]==list(reversed(atoms))
                if flag1 or flag2: 
                    found = True
            if not found:
                bond_types += [atoms]
        return bond_types



    def find_angle_types(self,atom_labels,angles):
        angle_types = []
        for angle in angles:
            atoms = [atom_labels[angle[0]-1],
                     atom_labels[angle[1]-1],
                     atom_labels[angle[2]-1]]
            found = False
            for i in range(len(angle_types)):
                flag1 = angle_types[i]==atoms
                flag2 = angle_types[i]==list(reversed(atoms))
                if flag1 or flag2: 
                    found = True
            if not found:
                angle_types += [atoms]
        return angle_types

    def find_improper_types(self,atom_labels,impropers):
        improper_types = []
        for improper in impropers:
            atoms = [atom_labels[improper[0]-1],
                     atom_labels[improper[1]-1],
                     atom_labels[improper[2]-1],
                     atom_labels[improper[3]-1]]
            found = False
            for improper_type in improper_types:
                flag1 = improper_type[0]==atoms[0]
                flag2 = set(atoms[1:4]) == set(improper_type[1:4])
                if flag1 and flag2: 
                    found = True
            if not found:
                improper_types += [atoms]
        return improper_types

