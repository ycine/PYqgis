# ZLICZANIE WARSTW W QGIS
# layers = iface.mapCanvas().layers()
# t = 0
# for i in layers:
#     t+=1
#
# import os, sys
# from qgis.core import *
#
layers = iface.mapCanvas().layers()
# #groups = qgis.subLayerCount.layers()
# u = QgsMapLayerRegistry
# c = 0
# for i in layers:
#     b = i.featureCount()
#     print(i.name)
#     print (b)
#     c += 1
#
# print("warstw:"+ str(c))

tiff = "E:\ASC\DANE GiS\ppp_2020_1km_Aggregated.tif"
tiff1add = iface.addRasterLayer(tiff,'')#dodawanie warstwy rastrowej

countries = r"E:\ASC\DANE GiS\ne_10m_admin_0_countries\0_countries.shp"
countries1add = iface.addVectorLayer(countries,'', 'ogr')
world_cities = r"E:\ASC\DANE GiS\World_Cities\World_Cities.shp"
world_cities1add = iface.addVectorLayer(world_cities,'','ogr')


#mozna odwolac sie do wczytany warstwy poprzez:
layer = iface.activeLayer()

if world_cities1add.isValid():
	print('yes')
else:
	print('no')


from qgis.core import *
countries = r"E:\ASC\DANE GiS\ne_10m_admin_0_countries\0_countries.shp"
world_cities = r"E:\ASC\DANE GiS\World_Cities\World_Cities.shp"
countries1add = QgsVectorLayer(countries,'countries','ogr')#przydalobysie nazwe nadac
world_cities1add = QgsVectorLayer(world_cities,'cities','ogr')
QgsProject.instance().mapLayers()#to pokaze elementy z QgsProject

for i in countries1add.fields():    #pokazuje pola z warstwy
	print(i.name(), i.typeName())

#to ma byc iteracja po warstwach w dokumentacji nazwana most common
fi = countries1add.getFeatures()
for i in fi:
	print('ajdi:', i.id())

countries1add.removeSelection() #odznacz wszystkie
countries1add.selectAll()
countries1add.selectByExpression("\"ADM0_A3\"='USA'", QgsVectorLayer.SetSelection)#wybiera obiekty wedlug zadanego atrybutu pole musi byc w "" natomiast wartosc w ''


#jezeli nie byly wczesniej zdefiniowane warstwy mozna sie do nich odwolac poprzez:
QgsProject.instance().mapLayers(0).values()
c = QgsProject.instance().mapLayersByName('0_countries')
print(c)
c[0].selectByExpression("\"ADM0_A3\"='USA'" , QgsVectorLayer.SetSelection)#tak dalej mozemy iterowac po warstwach
#powyzszy wybor warstwy dotyczy w przypadku jednej warstwy jezeli chcemy sie dobrac po indeksie to musimy uzyc:
t = iface.mapCanvas().layers()

t[0].selectByExpression("\"SOVEREIGNT\"='Venezuela'" , QgsVectorLayer.SetSelection)#selekcja po atrybutach
countries1add.selectByExpression("\"TYPE\"='Country'" , QgsVectorLayer.SetSelection)
world_cities1add.selectByExpression("\"STATUS\"='National and provincial capital'" , QgsVectorLayer.SetSelection)
select = countries1add.selectedFeatures()#subselekcja wybierz z zaznaczonych
for i in select:
	countries1add.selectByExpression("\"SOV_A3\"='GB1'", QgsVectorLayer.SetSelection)

#iteracja po kazdym obiekcie w warstwie po id
c = []
for i in rivers.getFeatures():
    c.append(i[0])

for z in c:
    lupa = '"id" = %i' % (z)
    rivers.selectByExpression(lupa, QgsVectorLayer.SetSelection)
    print(lupa)

#podobnie jak wyzej selekcja po kazdym obiekcie i dodatkowo selekcja po lokalizacji z zaznaczonych
c = []
for i in countries.getFeatures():
    c.append("'" + i[8] + "'")

for z in c:
    lupa = '"ADMIN" = %s' % (z)
    cc = countries.selectByExpression(lupa, QgsVectorLayer.SetSelection)
    for i in countries.selectedFeatures():
        pp = processing.run("native:selectbylocation",
                            {'INPUT': rivers, 'INTERSECT': QgsProcessingFeatureSourceDefinition('0_countries', True),
                             'METHOD': 0, 'PREDICATE': [0]})
    print(lupa)



#help do processingu
for alg in QgsApplication.processingRegistry().algorithms():
        print(alg.id(), "->", alg.displayName())
# help do processingu
processing.algorithmHelp("native:buffer")

import processing#select by location
processing.run("native:selectbylocation",  {'INPUT':countries1add,'PREDICATE':[0],'INTERSECT':world_cities1add,'METHOD':0}) # to zaznacz wszystko
processing.run("native:selectbylocation",  {'INPUT' :world_cities1add, 'INTERSECT' :QgsProcessingFeatureSourceDefinition('0_countries',True), 'METHOD' : 0, 'PREDICATE' : [0] })# zeby byla mozliwosc zaznaczenia tych warstw z zaznaczonych to 2 warstwa musi byc podana z nazwy z tabeli nie instancja czy jakos tak
processing.run("native:selectbylocation",  {'INPUT' :world_cities1add, 'INTERSECT' :QgsProcessingFeatureSourceDefinition(countries,True), 'METHOD' : 0, 'PREDICATE' : [0] })#tak tez dziala

#buffer
processing.run("native:buffer", { 'DISSOLVE' : False, 'DISTANCE' : 10, 'END_CAP_STYLE' : 0, 'INPUT' : QgsProcessingFeatureSourceDefinition(countries, False), 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'C:\Users\Marcin Wiaderkowicz\Desktop\roboczy\BUFBUF.shp', 'SEGMENTS' : 5 }) # tutaj trzeba podac sciezke wyjsciowa dla warstwy
processing.run("native:buffer", { 'DISSOLVE' : False, 'DISTANCE' : 10, 'END_CAP_STYLE' : 0, 'INPUT' : QgsProcessingFeatureSourceDefinition('World_Cities', True), 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'memory:', 'SEGMENTS' : 5 })
processing.runAndLoadResults("native:buffer", { 'DISSOLVE' : False, 'DISTANCE' : 10, 'END_CAP_STYLE' : 0, 'INPUT' : QgsProcessingFeatureSourceDefinition(countries, True), 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'C:/Users/Marcin Wiaderkowicz/Desktop/roboczy/BUFBUF.shp', 'SEGMENTS' : 5 })# to utworzy buffer w okreslonej lokalizacji i doda go do warstw
processing.runAndLoadResults("saga:splitlinesatpoints", { 'EPSILON' : 0, 'INTERSECT' : 'TEMPORARY_OUTPUT', 'LINES' : 'E:\\ASC\\DANE GiS\\10m_physical\\ne_10m_rivers_europe.shp', 'OUTPUT' : 1, 'SPLIT' : 'E:\\ASC\\DANE GiS\\World_Cities\\World_Cities.shp' })# tutaj istotne jest to ze jest inny dostawca alogrytmu nie native tylko saga jest to widoczne w panelu algorytmow
>>> processing.runAndLoadResults("gdal:pointsalonglines", { 'DISTANCE' : 0.5, 'GEOMETRY' : 'geometry', 'INPUT' : 'E:\\ASC\\DANE GiS\\10m_physical\\ne_10m_rivers_europe.shp', 'OPTIONS' : '', 'OUTPUT' : 'TEMPORARY_OUTPUT' })#tutaj narzedzie od gdal


caps_string = countries1add.dataProvider().capabilities()#to musi byc wykonane na warstwie przed dodawaniem kolumn czy wartosci
if caps_string & QgsVectorDataProvider.AddAttributes:#dodawanie kolumn do warstwy
	added1 = countries1add.dataProvider().addAttributes([QgsField('Order', QVariant.String),
	QgsField('Leno', QVariant.String)])
	countries1add.updateFields()

if caps_string & QgsVectorDataProvider.AddAttributes:#tylko takie typy pol mozna aktualnie dodawac
	added1 = t[1].dataProvider().addAttributes([QgsField('Order_of_blue_tunic', QVariant.Int),
	QgsField('Red_Order_of_blood', QVariant.Double),
    QgsField('Red_Order_of_green_hood', QVariant.String)])
	t[1].updateFields()

if caps_string & QgsVectorDataProvider.AddFeatures:#dodawanie wartosci do warstwy
    feat = QgsFeature(countries1add.fields())
    feat.setAttributes([2, 'cze']) #tutaj po przecinku sa kolejne pola w warstwie, jak sie zle wprowadzi albo wcale to bedzie puste albo 0
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(123, 456)))
    (res, outFeats) = world_cities1add.dataProvider().addFeatures([feat])

if caps_string & QgsVectorDataProvider.AddFeatures:#dodwawanie poligonu do warstwy poligonowej z danymi atrybutami
    feat = QgsFeature(t[1].fields())
    feat.setAttributes([4,6,6,'cze'])
    feat.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(12,34), QgsPointXY(16,34),QgsPointXY(12,45),QgsPointXY(16,45)]]))
    (res, outFeats) = t[1].dataProvider().addFeatures([feat])


if caps_string & QgsVectorDataProvider.DeleteFeatures: #usuwanie obiektow
    res = world_cities1add.dataProvider().deleteFeatures([2534]) #tutaj trzeba sie przyjrzec bo to nie jest to pierwsze pole w tabeli


if caps_string & QgsVectorDataProvider.DeleteAttributes:   #usuwanie pol
    res = world_cities1add.dataProvider().deleteAttributes([1])

lis = []
for i in coun.selectedFeatures():
    lis.append(i.id())
if caps_string & QgsVectorDataProvider.DeleteAttributes:   #usuwanie wielu pol
    res = world_cities1add.dataProvider().deleteAttributes(lis)

world_cities1add.updateFields()# to trzeba wykonac po kazdym usunieciu pola bo samo sie nie zatwierdza

t[0].selectedFeatureCount()#zlicz wszystkie zaznaczone obiekty


for i in t[1].selectedFeatures(): #edycja atrybutow warstwy
    if caps_string & QgsVectorDataProvider.ChangeAttributeValues:
        id = i.id()
        attrs = {94:'666'}
        t[1].dataProvider().changeAttributeValues({id:attrs})

for i in t[0].selectedFeatures():#drukuje id warstwy dla kazdego obiektu
	print(i.id())


dl = range(1,100)
for i in dl: # dodaje atrybuty do wszystkich obiektow z podanym id
    if caps_string & QgsVectorDataProvider.ChangeAttributeValues:
        attrs = {94:'667'} #tutaj pierwsza wartosc to index pola, druga wartosc to  wartosc jaka ma byc wprowadzona do pola
        t[1].dataProvider().changeAttributeValues({i:attrs}) #i - czyli numer obietku ? w sensie id ?

# to zwraca dlugosc geometrii z danej warstwy
for i in rivers.getFeatures():
    geom = i.geometry()
    print('geometria: ', i.id(), geom.length())

#GOTOWIEC!

countries = r"E:\ASC\DANE GiS\ne_10m_admin_0_countries\0_countries.shp"
countries1add = iface.addVectorLayer(countries,'', 'ogr')
world_cities = r"E:\ASC\DANE GiS\World_Cities\World_Cities.shp"
world_cities1add = iface.addVectorLayer(world_cities,'','ogr')

if world_cities1add.isValid():
	print('yes')
else:
	print('no')

fi = countries1add.getFeatures()
for i in fi:
	print('ajdi:', i.id())

countries1add.selectByExpression("\"SOVEREIGNT\"='Venezuela'", QgsVectorLayer.SetSelection)
processing.run("native:selectbylocation",  {'INPUT' :world_cities1add, 'INTERSECT' :QgsProcessingFeatureSourceDefinition(countries,True), 'METHOD' : 0, 'PREDICATE' : [0] })#tak tez dziala


#GOTOWIEC! selekcja wasrtwy ktora sie przecina z druga nastepnie update atrybutow w tej warstwie na podstawie drugiej
c = []
caps_string = rivers.dataProvider().capabilities()
for i in countries.getFeatures():
    c.append("'" + i[8] + "'")

for z in c:
    lupa = '"ADMIN" = %s' % (z)
    cc = countries.selectByExpression(lupa, QgsVectorLayer.SetSelection)
    for i in countries.selectedFeatures():

        pp = processing.run("native:selectbylocation",
                            {'INPUT': rivers, 'INTERSECT': QgsProcessingFeatureSourceDefinition('0_countries', True),
                             'METHOD': 0, 'PREDICATE': [0]})

        for i in rivers.selectedFeatures():  # edycja atrybutow warstwy

            if caps_string & QgsVectorDataProvider.ChangeAttributeValues:
                id = i.id()
                attrs = {14: z}
                rivers.dataProvider().changeAttributeValues({id: attrs})

    print(lupa)