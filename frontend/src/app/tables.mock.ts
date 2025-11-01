export type Table = {
  id: number;
  status: 'available' | 'occupied';
  number_of_people: number;
};

export const mockTables: Table[] = [
  { id: 1, status: 'available', number_of_people: 0 },
  { id: 2, status: 'available', number_of_people: 0 },
  { id: 3, status: 'available', number_of_people: 0 },
  { id: 4, status: 'available', number_of_people: 0 },
  { id: 5, status: 'available', number_of_people: 0 },
  { id: 6, status: 'available', number_of_people: 0 },
  { id: 7, status: 'available', number_of_people: 0 },
  { id: 8, status: 'available', number_of_people: 0 },
  { id: 9, status: 'available', number_of_people: 0 },
  { id: 10, status: 'available', number_of_people: 0 },
];