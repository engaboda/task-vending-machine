from rest_framework.exceptions import APIException


class ProductPriceIsLargerThanUserDeposit(APIException):
    status_code = 400
    default_detail = 'Cost of Product is larger than Available Price'
    default_code = 'Cost_of_Product_is_larger_than_available_price'


class ProductNumberIsLargerThanProductAvailable(APIException):
    status_code = 400
    default_detail = 'Product Number Is Larger Than Product Available'
    default_code = 'product_number_is_larger_than_product_available'
