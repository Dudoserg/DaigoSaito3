#kek
from django.conf import settings
from django.core.files import File
from django.shortcuts import render
from blog.models import Material, Technology_map, Technology_map_position, Product
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.urls import reverse

from blog.models import Document
from blog.forms import DocumentForm

from django.conf.urls.static import static
from django.conf import settings as djangoSettings

from django.views.generic import ListView
from django.db.models import Q

import hashlib
from PIL import Image
#import Image
import io
import os

import json

from django.contrib import auth
from django.db.models import Count


# Create your views here.


#
# def post_list(request, pk ):
#
#     return render(request, 'blog/example/post_list.html', {})

#
    # class PlaceListView(ListView):
    #
    #     model = Place

#
# @csrf_exempt
# def get_queryset(request):
# # Получаем не отфильтрованный кверисет всех моделей
#
#
#     # q_list = [Q(question__startswith='Who'), Q(question__startswith='What')]
#     # products = Product.objects.filter
#     #
#     #
#     # queryset = super (FlavorListView, self).get_queryset()
#     # q = self.request.GET.get("q")
#     # if q: # Если 'q' в GET запросе, фильтруем кверисет по данным из 'q'
#     #     return queryset.filter(Q(name__icontains=q)| Q(keywords__icontains=q))
#     #
#     # title = request.POST["Prods"]
#     lst = request.POST['Prods']
#     products = Product.objects.all()[0]
#     # products = Product.objects.filter(id=1)[0]
#
#     data = {'products': products}
#     lst = render (request, 'blog/ProductsBlock.html', context=data)
#     # return render (request, 'blog/ProductsBlock.html', context=data)
#


#


# Страница со всеми продуктами
@csrf_exempt
def product(request):

    products = Product.objects.all()

    if 'myInput' in request.GET:
        print(request.GET['myInput'])

    # Если используем поиск, запрос которого пришел по аяксу
    if 'data' in request.GET:
        print("ajax")
        dataFromJson = foobar(request.GET['data'])
        inputField = dataFromJson['input']
        arrCheckBox = dataFromJson['arr']
        print(inputField)
        for i in range(0, len(arrCheckBox)):
            print(arrCheckBox[i])

        list = arrCheckBox
        q_objects = Q()
        for item in list:
            q_objects.add(Q(material__id=item), Q.OR)
        # получаем все позиции тех карты, в которых указаны нужные нам материалы
        map_position = Technology_map_position.objects.filter(q_objects)
        for i in range(0, len(map_position)):
            print("technology_map_id = " + str(map_position[i].technology_map_id) + "  amount = " + str(
                map_position[i].amount))
         # по даунски отбираю айдишники technology_map_id чтоб не повторялись
        ids = []
        for i in range(0, len(map_position)):
            if (map_position[i].technology_map_id not in ids):
                ids.append(map_position[i].technology_map_id)

        list = ids
        q_objects = Q()
        for item in list:
            q_objects.add(Q(id=item), Q.OR)##############################################################
        # получили все карты, в которых присутствуют нужные материалы
        map = Technology_map.objects.filter(q_objects)
        # получили все айдишники продуктов, в которых материалы нужные
        productId = []
        [ productId.append(i.product_id) for i in map]

        list = productId
        q_objects = Q()
        for item in list:
            q_objects.add(Q(id=item), Q.OR)
        # получаем нужные продукты для вывода
        products = Product.objects.filter(q_objects)

        # Теперь займемся поиском по словам
        lenght = len(inputField)

        q_objects = Q()
        if(len(inputField) > 0):
            q_objects.add(Q(title__contains=inputField), Q.OR)
            q_objects.add( Q(description__contains=inputField), Q.OR)

        if dataFromJson['code']:
            count = int(dataFromJson['code'])
            q_objects.add(Q(code=count), Q.AND)
        if dataFromJson['amountFrom']:
            amountFrom = int(dataFromJson['amountFrom'])
            q_objects.add(Q(), Q.AND)
        if dataFromJson['amountFrom']:
            amountFrom = int(dataFromJson['amountFrom'])
            q_objects.add(Q(balance__gte=amountFrom), Q.AND)
        if dataFromJson['amountTo']:
            amountTo = int(dataFromJson['amountTo'])
            q_objects.add(Q(balance__lte=amountTo), Q.AND)
        # if(lenght > 5):
        products = products.filter(q_objects)


        allMaterials = Material.objects.all()
        data = {'products': products, 'materials': allMaterials, 'username' :auth.get_user(request).username}
        return render(request, 'blog/search.html', context=data)
    else:
        allMaterials = Material.objects.all()
        data = {'products': products, 'materials': allMaterials,  'username' :auth.get_user(request).username}
        return render(request, 'blog/allProduct.html', context=data)

def foobar(json1):
    msg = json.loads(json1)
    return msg

# Страница с конкретным продуктом
def productPage(request, id):

    product = Product.objects.filter(id=id)[0]

    map = Technology_map.objects.filter(product_id=id)
    len = map.__len__()

    if( len != 0):
        map = map[0]
        print("mapId " + str(map.id))
        print(" ")

        map_position = Technology_map_position.objects.filter(technology_map_id=map.id)
        len = map_position.__len__()

        for i in range(0, map_position.__len__()):
            print("id " + str(map_position[i].id))
            print("material " + str(map_position[i].material_id))
            print("amount " + str(map_position[i].amount))
            print("technology_map " + str(map_position[i].technology_map_id))
            print(" ")

        print("productTitle" + str(product.title))

        data = {'product' : product,
                'mapPositions' : map_position,
                'username': auth.get_user(request).username
                }
        return render(request, 'blog/product.html', context=data)
    else:
        data = {'product': product,
                'mapPositions': [],
                'username': auth.get_user(request).username
                }
        return render(request, 'blog/product.html', context=data)

# Cтраница для редактирования продукта
@csrf_exempt
def productEdit(request, idparam):

    username = auth.get_user(request).username
    if not username:
        return render(request, 'blog/NoAccess.html')


    product = Product.objects.filter(id= idparam)
    product = product[0]

    # Если в запросе есть картинка
    if ('image' in request.FILES):
        up_file = request.FILES['image']
        print(up_file)
        tmpName = "tmp.jpg"
        destination = open(djangoSettings.IMG_ROOT + "/" + tmpName, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()
        #img = someImage()

        img = Image.open(djangoSettings.IMG_ROOT + "/" + tmpName)

        m = hashlib.md5()
        with io.BytesIO() as memf:
            img.save(memf, 'PNG')
            data = memf.getvalue()
            m.update(data)
        print(m.hexdigest())
        # переименовываем загруженный файл
        newName = str(m.hexdigest()) + ".jpg"
        # если файл существует
        if(os.path.exists(djangoSettings.IMG_ROOT + "/" + newName) == True):
            # удалим файл
            os.remove(djangoSettings.IMG_ROOT + "/" + newName)

        os.rename(djangoSettings.IMG_ROOT + "/" + tmpName, djangoSettings.IMG_ROOT + "/" + newName)
        # save to bd
        product.img = "img/" + newName
        product.save()

    print("product.img == " + str(product.img))
    print("product.title == " + str(product.title))
    materials = Material.objects.all()

    map = Technology_map.objects.filter(product_id=idparam)
    if len(map) > 0:
        map = map[0]

        positions = Technology_map_position.objects.filter(technology_map_id=map.id)
        idishnik = map.id
        data = {'product' : product,
                'materials' : materials,
                'positions' : positions,
                'idMap': idishnik, 'username' :auth.get_user(request).username}

        return render(request, 'blog/test.html', context=data)
    else:
        # нужно добавить новую карту
        technology_map = Technology_map()
        technology_map.date_start = "2019-03-09"
        technology_map.date_end = "2019-03-09"
        technology_map.product_id = idparam
        technology_map.save()
        idishnik = technology_map.id
        data = {'product': product,
                'materials': materials,
                'positions': [],
                'idMap' : idishnik, 'username' :auth.get_user(request).username}

        return render(request, 'blog/test.html', context=data)
# выполняет редактирование информации о продукте через Аjax
@csrf_exempt
def productEditajax(request, idparam):
    # print("startEditAjax")
    # print(idparam)

    username = auth.get_user(request).username
    if not username:
        return render(request, 'blog/NoAccess.html')

    title = request.POST['title']
    #print(title)
    code = request.POST['code']
    #print(code)
    balance = request.POST['balance']
    #print(balance)
    description = request.POST['description']
    #print(description)

    # получаем нужную  нам  модель продукта из базы
    product = Product.objects.get(id=idparam)
    # редактируем ее
    product.title = title
    product.code = code
    product.balance = balance
    product.description = description
    # сохраняем
    product.save()

    return HttpResponse("Success!")

@csrf_exempt
def productAddMaterial(request, idparam):

    username = auth.get_user(request).username
    if not username:
        return render(request, 'blog/NoAccess.html')

    amount = 1
    material_id = request.POST['idMaterial']
    technology_map_id = request.POST['idMap']

    technology_map_position = Technology_map_position()

    technology_map_position.amount = amount

    tmp = Material.objects.filter(id=material_id)[0]
    technology_map_position.material = tmp

    tmp = Technology_map.objects.filter(id=technology_map_id)[0]
    technology_map_position.technology_map = tmp

    technology_map_position.save()

    data = {'positionMap': technology_map_position, 'username' :auth.get_user(request).username}

    return render(request, 'blog/onePositionMap.html', context=data)

@csrf_exempt
def productEditPosition(request, idparam):
    username = auth.get_user(request).username
    if not username:
        return render(request, 'blog/NoAccess.html')

    print("id == " + str(request.POST['id']))
    idMaterial = request.POST['id']
    amount = int(request.POST['amount'])
    position = Technology_map_position.objects.filter(id=idMaterial)[0]
    if( amount > 0):
        position.amount = amount
        position.save()
        return HttpResponse("Success!")
    else:
        position.delete()
        return HttpResponse("Element deleted!")



# def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile = request.FILES['docfile'])
#             newdoc.save()
#
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('myapp.views.list'))
#     else:
#         form = DocumentForm() # A empty, unbound form
#
#     # Load documents for the list page
#     documents = Document.objects.all()
#
#     # Render list page with the documents and the form
#     return render_to_response(
#         'myapp/list.html',
#         {'documents': documents, 'form': form},
#         context_instance=RequestContext(request)
#     )

def base(request):

    username = auth.get_user(request).username
    if username:
        print("Пользователь ВОШЕЛ  " + str(username))
    else:
        print("Пользователя НЕТ")

    data = { 'username': auth.get_user(request).username}
    return render(request, 'blog/example/post_list.html', context=data)

@csrf_exempt
def product_delete(request):

    username = auth.get_user(request).username
    if not username:
        return render(request, 'blog/NoAccess.html')

    if request.POST.get('num'):
        num =  request.POST['num']
        print(num)
        str = Product.objects.filter(id=num)[0].title
        product = Product.objects.get(id=num).delete()
        return HttpResponse("Element " + str + " deleted!")
    else:
        return HttpResponse("Error2")

@csrf_exempt
def productAdd(request):

    username = auth.get_user(request).username
    if not username:
        return render(request, 'blog/NoAccess.html')

    if 'title' in request.POST and 'code' in request.POST and 'balance' in request.POST and 'description' in request.POST:
        lenght = len(request.FILES)
        if lenght > 0:
            # обрабатываем и сохраняем картинку
            elem = request.FILES.get('0')
            name = saveFile(elem)
            print(name)
            # теперь инфомарцию о продукте
            print("ajax")
            title = (request.POST['title'])
            print(title)
            code = (request.POST['code'])
            print(code)
            balance = (request.POST['balance'])
            print(balance)
            description = (request.POST['description'])
            print(description)
            newProduct = Product()
            newProduct.title = title
            newProduct.code = code
            newProduct.balance = balance
            newProduct.description = description
            newProduct.img = "img/" + name
            newProduct.save()

    data = {'username': auth.get_user(request).username}
    return render(request, 'blog/productAdd.html', context=data)


def saveFile(up_file):
    #print(up_file)
    tmpName = "tmp.jpg"
    destination = open(djangoSettings.IMG_ROOT + "/" + tmpName, 'wb+')
    for chunk in up_file.chunks():
        destination.write(chunk)
    destination.close()
    # img = someImage()

    img = Image.open(djangoSettings.IMG_ROOT + "/" + tmpName)

    m = hashlib.md5()
    with io.BytesIO() as memf:
        img.save(memf, 'PNG')
        data = memf.getvalue()
        m.update(data)
    #print(m.hexdigest())
    # переименовываем загруженный файл
    newName = str(m.hexdigest()) + ".jpg"
    # если файл существует
    if (os.path.exists(djangoSettings.IMG_ROOT + "/" + newName) == True):
        # удалим файл
        os.remove(djangoSettings.IMG_ROOT + "/" + newName)

    os.rename(djangoSettings.IMG_ROOT + "/" + tmpName, djangoSettings.IMG_ROOT + "/" + newName)
    return newName