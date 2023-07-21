import yappi
yappi.set_clock_type('wall')

def read_file(src):
    with open(src, encoding='utf-8') as fd:
        return fd.read().splitlines()
    
def find_duplicates(src='products.txt'):
    products = read_file(src)
    products = [product.lower() for product in products]
    products.sort()
    duplicates = [product1 for product1, product2 in zip(products[:-1], products[1:]) if product1 == product2]
    return duplicates

yappi.start(builtins=True)
find_duplicates()
yappi.stop()

ypstats = yappi.get_func_stats()
ypstats.sort(sort_type='ttot', sort_order="desc")
ypstats.print_all()

ver = 'products4'
ypstats.save(f"./stats/stats_pver_{ver}.stats", type="pstat")

