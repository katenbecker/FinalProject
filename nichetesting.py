import unittest
from niche import *


class TestingDataBases(unittest.TestCase):

	def testNameTable(self):
		conn = sqlite.connect('schools.sqlite')
		cur = conn.cursor()

		sql = '''SELECT UniversityName, State, Rank, AcceptanceRate
				From Names 
				WHERE State = "california" '''
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 23)
		self.assertEqual(result_list[4][3], 13)
		self.assertEqual(result_list[8][2], 65)


	def testNumberInfoTable(self):
		conn = sqlite.connect('schools.sqlite')
		cur = conn.cursor()

		sql = '''SELECT UniversityName, Students, InStateTuition, OutStateTuition
				From NumberInfo 
				WHERE UniversityName = "Wayne State University" '''
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(result_list[0][1], "12,003")
		self.assertEqual(result_list[0][2], "12,269")
		self.assertEqual(result_list[0][3], "26,220")

class TestingJoiningTables(unittest.TestCase):

	def testRandomUni(self):
		conn = sqlite.connect('schools.sqlite')
		cur = conn.cursor()

		sql = '''SELECT i.UniversityName, i.Students, n.Rank, n.State
                    FROM Names as n
                    JOIN NumberInfo as i
                    ON n.UniversityName = i.UniversityName
                    WHERE i.UniversityName ="University of the Sciences"'''
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(result_list[0][1], "1,325")
		self.assertEqual(result_list[0][2], 389)
		self.assertEqual(result_list[0][3], "pennsylvania")

	def testAnotherRandom(self):
		conn = sqlite.connect('schools.sqlite')
		cur = conn.cursor()

		sql = '''SELECT n.UniversityName, i.InStateTuition, i.OutStateTuition
                    FROM NumberInfo as i
                    JOIN Names as n
                    ON n.UniversityName = i.UniversityName
                    WHERE n.State = "washington"'''
		results = cur.execute(sql)
		result_list = results.fetchall()

		self.assertEqual(result_list[0][0], "University of Washington")
		self.assertEqual(result_list[3][1], "40,562")
		self.assertEqual(result_list[10][2], "34,869")


class Testing_get_colleges(unittest.TestCase):

	def testing_function(self):
		getting_colleges = get_colleges_for_state('ia')
		self.assertEqual(getting_colleges[0]['uni_rank'], '67')
		self.assertEqual(getting_colleges[2]['acceptance_rate'], "87%")
		self.assertEqual(getting_colleges[4]['uni_name'], "Drake University")

	def testing_another(self):
		getting_colleges = get_colleges_for_state('mt')
		self.assertEqual(getting_colleges[1]['uni_name'], 'Montana Tech of the University of Montana')
		self.assertEqual(getting_colleges[2]['students'], "12,248")
		self.assertEqual(getting_colleges[4]['acceptance_rate'], "62%")
		


unittest.main()



