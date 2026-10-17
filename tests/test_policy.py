import unittest
from decimal import Decimal
from policy import Claim, route, equal_split, monthly_cost

class PolicyTests(unittest.TestCase):
    def test_review_boundary(self):
        self.assertEqual(route(Claim(50000,.9,True,True)), 'eligible_for_approval')
        self.assertEqual(route(Claim(50001,.9,True,True)), 'human_review')
    def test_unverified_fields_block(self):
        self.assertEqual(route(Claim(100,.84,True,True)), 'request_information')
        self.assertEqual(route(Claim(100,.99,False,True)), 'request_information')
    def test_policy_rejection(self):
        self.assertEqual(route(Claim(100,.9,True,False)), 'reject')
    def test_split_preserves_cents(self):
        self.assertEqual(equal_split(100,3),(34,33,33))
    def test_cost(self):
        self.assertEqual(monthly_cost(1000,.02,.1,5,60,100),Decimal('620.00'))
    def test_invalid_amount(self):
        with self.assertRaises(ValueError): route(Claim(-1,.9,True,True))

if __name__ == '__main__': unittest.main()
