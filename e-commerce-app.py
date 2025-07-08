from datetime import datetime
orders = []

class ShippingService:
    def shipmentNotice(self,prods):
        print("** Shipment Notice **")
        total = 0
        for item,q in prods.items():
            name = item.getName()
            quantity = q[0]
            weight = q[1]
            total += quantity*weight
            print(f"{quantity:2}x {name:12} {quantity*weight:4}Gram")
        print("-------------------------")
        print(f"total package weight {total:>16.2f}")


class ProductCreator:           ### product factory useful for scability
    all = []
    @classmethod
    def create(cls):
        print("plese enter following data")
        print("------------------------------------------------")
        name = input("enter name of product : ")
        stock = int(input(f"enter how much stock of {name} : "))
        price = float(input(f"enter price of {name} : "))
        is_phy = input(f"is {name} a physical product (T/F) : ") == "T"
        is_expiring = False
        weight = None
        expire_date = None

        if is_phy: #if product is physical then it has weight and could have expiring date
            weight = float(input(f"enter weight of {name} : "))
            is_expiring = input(f"Does {name} have an expiration date? (T/F) : ") == "T"
            if is_expiring:expire_date=input(f"enter expiration date of {name} (ex:2025-08-18)  : ")

        p = Product(name,stock,price,is_phy,is_expiring,weight,expire_date)
        cls.all.append(p)
        return p

class CustomerRegister:   ### User factory
    all = []
    @classmethod    
    def create(cls):
        print("plese enter following data")
        print("------------------------------------------------")
        name = input("enter user name : ")
        balance = float(input("enter user balance : "))
        user = Customer(name,balance) 
        cls.all.append(user)
        return user



class Product :
    object = ProductCreator
    def __init__(self,name,stock,price,is_phy,is_expiring,weight,expire_date):
        self.__name = name
        self.__stock = stock
        self.__price = price
        self.__is_physical = is_phy
        self.__weight = weight if weight else None
        self.__is_expiring = is_expiring
        self.__expire_date = expire_date

    def __str__(self):
        return self.__name

    def getName(self):
        return self.__name

    def getPrice(self):
        return self.__price
    
    def is_expiring(self):
        return (self.__is_expiring,self.__expire_date)

    def is_physical(self):
        return (self.__is_physical,self.__weight)
    
    def getStock(self):
        if self.__is_expiring:
            expire_date = datetime.strptime(self.__expire_date, "%Y-%m-%d")
            now = datetime.now()
            if expire_date < now:
                return 0
        return self.__stock



class Customer:
    object = CustomerRegister
    def __init__(self,name,balance):
        self.__name = name
        self.__balance = balance

    def __str__(self):
        return self.__name
    def getBalance(self):
        return self.__balance
    def makePurchase(self,bill):
        self.__balance-=bill
        return self.__balance
        


class Cart:
    def __init__(self):
        self.__prods = {}
    
    def add(self,product,quantity):
        if product in self.__prods:
            self.__prods[product] += quantity 
        else : self.__prods[product] = quantity

    def getProducts(self):
        return self.__prods 

    def remove(self,product):
        if product in self.__prods: 
            del self.__prods[product]
            return True
        else: return False
        
def receipt(items,total,balance):
    print("** Checkout receipt **")
    for item,q in items.items():
        name = item.getName()
        price = item.getPrice()
        print(f"{q:2}x {name:12} {q*price:4}$")
    print("-------------------------")
    print(f"subtotal {total:>13.2f}")
    print(f"shipping         30.00")
    total+=30
    print(f"total {total:>16.2f}")
    print(f"remaining balance {balance}")


def checkout(customer,cart):
    total = 0
    shipment = {}

    for product,quantity in cart.getProducts().items():
        stock = product.getStock()
        if stock<quantity:
            print ("unable to make purchace you ordered ",quantity," whily only ",product.getStock()," in stock")
            return
        total += product.getPrice()*quantity
        is_phys,w = product.is_physical()
        if is_phys:
            ##add to shipping list
            shipment[product]= (quantity,w)

    if total == 0:
        print("cart is empty")
        return
    
    balance = customer.getBalance()
    if balance < total:
        print ("unable to make purchace total is ",total,"\nyour balance is ",balance)
        return
    else:
        balance = customer.makePurchase(total+30)

    order = ShippingService()
    order.shipmentNotice(shipment)   
    receipt(cart.getProducts(),total,balance)
    




if __name__=="__main__":
    user=Customer.object.create()
    cheese = Product.object.create()
    copon=Product.object.create()
    cart=Cart()
    cart.add(cheese,4)
    cart.add(copon,1)
    checkout(user,cart)
    print(Product.object.all) #you can access all existing products