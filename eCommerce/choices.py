from django.db import models


class ProductCatogary(models.TextChoices):
    phones = 'Phones', 'Phones'
    laptops = 'Laptops', 'Laptops'
    tablet = 'Tablets', 'Tablets'
    desktop_pc = 'Desktop pc', 'Desktop pc'


class ProductBrand(models.TextChoices):
    brand1 = 'Samsung', 'Samsung'
    brand2 = 'Apple', 'Apple'
    brand3 = 'Dell', 'Dell'
    brand4 = 'Sony', 'Sony'
    brand5 = 'Lenovo', 'Lenovo'
    brand6 = 'Moto','Moto'


class ProductSystem(models.TextChoices):
    sys1 = 'Android','Android'
    sys2 = 'iOS','iOS'
    sys3 = 'Windows','Windows'
    sys4 = 'Linux','Linux'
    sys5 = 'MacOS','MacOS'
    sys6 = 'iPadOS','iPadOS'
    sys7 = 'Chrome OS','Chrome OS'


class Status(models.TextChoices):
    s1 = 'Order Taken','Order Taken'
    s2 = 'Order is Being Prepared','Order is Being Prepared'
    s3 = 'Order Is Being Delivered','Order Is Being Delivered'
    s4 = 'Order Received'


class Gender(models.TextChoices):
    g1 = 'Male','Male'
    g2 = 'Female','Female'


class City(models.TextChoices):
    c1 = 'Baghdad','Baghdad'
    c2 = 'Najaf','Najaf'
    c3 = 'Basra','Basra'
    c4 = 'Al-Qadisiyyah','Al-Qadisiyyah'
    c5 = 'Al Muthanna','Al Muthanna'
    c6 = 'Maysan','Maysan'
    c7 = 'Wasit','Wasit'
    c8 = 'Karbala','Karbala'
    c9 = 'Sulaymaniyah','Sulaymaniyah'
    c10 = 'Dihok','Dihok'
    c11 = 'Saladin','Saladin'
    c12 = 'Diyala','Diyala'
    c13 = 'Al Anbar','Al Anbar'
    c14 = 'Kirkuk','Kirkuk'
    c15 = 'Dhi Qar','Dhi Qar'
    c16 = 'Erbil','Erbil'
    c17 = 'Nineveh','Nineveh'
    c18 = 'Babylon','Babylon'


