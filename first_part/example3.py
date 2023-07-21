import yappi
yappi.set_clock_type('wall')

def read_file(src):
    with open(src, encoding='utf-8') as fd:
        return fd.read().splitlines()
        
def find_duplicates(src='products.txt'):
    products = read_file(src)
    products = [product.lower() for product in products]
    # Создаем пустой списоку для хранения дубликатов
    duplicates = []
    while products:
        # Извлекаем последний элемент из списка
        product = products.pop()
        if product in products:
            # Пополняем список дубликатов
            duplicates.append(product)
    return duplicates  

yappi.start(builtins=True)
find_duplicates()
yappi.stop()

ypstats = yappi.get_func_stats()
ypstats.sort(sort_type='ttot', sort_order="desc")
ypstats.print_all()

ver = 'products3'
ypstats.save(f"./stats/stats_pver_{ver}.stats", type="pstat")

