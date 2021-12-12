from types import NoneType
from Field import Field
from FieldTypes import FieldType
from Player import Player

class Table:
	fieldMarks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

	def __init__(self, n, m):
		self.n = n
		self.m = m
		self.matrixRows = 2*n - 1
		self.matrixColumns = 2*m - 1
		self.matrix = []
		self.initFields()
		self.players = []

	def initFields(self):
		for i in range(self.matrixRows):
			self.matrix.append([])
			for j in range(self.matrixColumns):
				if i % 2 == 0:
					if j % 2 == 0:
						self.matrix[i].append(Field(i, j, FieldType.EMPTY, self))
					else:
						self.matrix[i].append(Field(i, j, FieldType.VERTICAL_WALL_EMPTY, self))
				else:
					if j % 2 == 0:
						self.matrix[i].append(Field(i, j, FieldType.HORIZONTAL_WALL_EMPTY, self))
					else:
						self.matrix[i].append(Field(i, j, FieldType.EMPTY, self))

	def printTable(self):
		n = self.n
		m = self.m

		print(*["==" for i in range(self.matrixColumns+4)], sep = "", end = "\n\n");

		print("    ", end = "")
		print(*self.fieldMarks[:m], sep = "   ")

		print("   ", end = "")
		print(*["===" for i in range(m)], sep = " ")

		for row in range(n):
			toPrint = f'{self.fieldMarks[row]} ǁ '

			i = row * 2
			for j in range(self.matrixColumns):
				toPrint += self.matrix[i][j].getSymbol()

			toPrint += f' ǁ {self.fieldMarks[row]}'

			i += 1
			if i < self.matrixRows:
				toPrint += "\n   "
				for j in range(self.matrixColumns):
					toPrint += self.matrix[i][j].getSymbol()
			
			print(toPrint)
			
		print("   ", end = "")
		print(*["===" for i in range(m)], sep = " ")
		print("    ", end = "")
		print(*self.fieldMarks[:m], sep = "   ")
		print(f'\nN = {n}, M = {m}', end = "\n\n")

	def createPlayer(self, type, row, column):
		newPlayer = Player(type, row, column, self)
		self.players.append(newPlayer)
		newPlayer.setPlayerOnTable()

	def getFieldByRowAndColumn(self, row, column):
		i = (row - 1) * 2
		j = (column - 1) * 2
		return self.matrix[i][j]

	def getFieldForWall(self, row, column, color):
		row = row - 1
		column = column -1
		if color == 'p':
			if row == 0:
				return NoneType
			try:
				return [self.matrix[row * 2 - 1][column * 2], self.matrix[row * 2 - 1][column * 2 + 2]]
			except:
				return NoneType
		elif color == 'z':
			if column == 0:
				return NoneType
			try:
				return [self.matrix[row * 2][column * 2 + 1], self.matrix[row * 2 + 2][column * 2 + 1]]
			except:
				return NoneType
		else:
			return NoneType


	def isGameFinished(self):
		for p in self.players:
			if p.isWinner():
				print(f"~~~~~~~~ {p.type.name} is WINNER!! ~~~~~~~~")
				return True
		return False

	def requestInputForPlayerPosition(self, sign, seqNumber):
		i = -1
		j = -1
		while(i < 1 or i > self.n or j < 1 or j > self.m):
			if i != -1 and (i < 1 or i > self.n):
				print(f'[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.n}. Vi ste uneli: ' + str(i))
			if j != -1 and (j < 1 or j > self.m): 
				print(f'[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.m}. Vi ste uneli: ' + str(j))

			print(f'Unesite poziciju za {seqNumber}. figuru igrača {sign} [Format: vrsta kolona (primer: 3 5)]: ', end = "")
			unos = input().split(" ")
			if len(unos) == 2 and unos[0].isnumeric() and unos[1].isnumeric():
				# TO-DO provera da li je polje vec zauzeto
				i = int(unos[0])
				j = int(unos[1])
			
		print(f'[{sign}({seqNumber})] Uneli ste poziciju ({i}, {j}).')
		return (i, j)


	def requestInputForWallPosition(self, sign):
		color = ''
		i = -1
		j = -1
		while(i < 1 or i > self.n or j < 1 or j > self.m or len(color) < 1):
			# TO-DO: treba da se uradi provera za unesenu boju zida
			# if color != '' and (color != 'p' or color != 'z'):
			# 	print(f'[GRESKA] Uneli ste neodgovarajucu boju za zid, pokusajte ponovo za karaktere [p, z]')
			# 	continue
			if i != -1 and (i < 1 or i > self.n):
				print(f'[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.n}. Vi ste uneli: ' + str(i))
			if j != -1 and (j < 1 or j > self.m): 
				print(f'[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.m}. Vi ste uneli: ' + str(j))

			print(f'Unesite poziciju za zid igrača {sign} [Format: boja (p, z) vrsta kolona (primer: p 6 5)]: ', end = "")
			unos = input().split(" ")
			if len(unos) == 3 and len(unos[0]) == 1 and unos[1].isnumeric() and unos[2].isnumeric():
				color = unos[0]
				i = int(unos[1])
				j = int(unos[2])
				field = self.getFieldForWall(i, j, color)
				if field != NoneType and len(field) > 0:
					if field[0].isWall() or field[1].isWall() or field[0].areWallsCrossing(color):
						print("Vec posotoji zid na ovoj poziciji")
						i = -1
						j = -1
						color = ''
					else:
						for f in field:
							f.setWall(color)
				else:
					print("Ne moze se uneti zid na tu poziciju")
					i = -1
					j = -1
					color = ''