from fetch_urls import fetch_urls
from data_scraper import data_extract_first_api, data_extract_second_api, html_scraper



search_item = input('What item do you want to search for?: ')
first_url, second_url = fetch_urls(search_item)

html_scraper(search_item)
data_extract_first_api(first_url)
data_extract_second_api(second_url)


## FUNCIONA LO DE CATCH LAS URL, AHORA REQUEST ESAS URLS I RECOGER DATA DE ELLAS - done

# could change the while true loop and use insted of _ in range len(items in the jnson) as in the first url it should be just 100-done
# After that could change that repetitive thing of changing offset number - done 

# use a loop in the firts get hidden api, somethimes cant find tthe url i think,  it is not associated with a value - done

## UNA FUNCION, PARA LA PRIMERA URL DEBERIA FUNCIONAR, DE MIRAR SI FUNCTIONA CON LA SEGUNDA URL- DEPENDIENDO EN LA STRUCTURA DE JSON - done

# ultimo - la funcion de extract data funciona solo con el primer json, no con el segundo. toca hacer para el segundo - done
# puedo reciclar codigo, delete.txt, para recojer ese loop, ir cambiando paginas etc - done

# despues de hacer le funcion para la segunda api emepzar a guradar datos - done

# catch error, buscando g29 no tengo muchos items y no hay boton de next, cazar cuando da ese error posible mente con un simple try catchs - hecho creo/ revisar mas terde  - done

# PROBLEMA !!! - hay item estaticos tmb, unos tmb con top favirtes que pueden venir de otra parte, no del endpoint - done
#puedo usar html scraper primero, y luego las dos hiddens api - done
#filtrar datos con id(lo que uso ahora) - done

#empezar a ordenar codigo ahora. es un poco messy - he separado la logica - main llama pide input y llama todo - fethc url consige las hidden api - json scraper recoge los datos de la funciones - done

# en el de recoger apis, el driver se ejetuca primero y no quiero, quiero que lo haga despues o talvez desactivar el texto y ya(mas facil chat gpt te ayuda) - no puedo, hacer wait en main y ya  - done

# prodria hacer el html scaper en su file y importarla a json scraper/talvez generalizar el file con data extract y meter las tres logicas ahi - parcialmente done creo

# necesito ir guardando las id de los itmes en las tres functiones, ese es el motivo para hacer esto - done creo

#tmb hacer que no printee cosas el selenium - no soy capaz. resuelto de otra manera - done


#mejorar el fetch de la segunda api, no esta bien hecha - en proceso


# crear nombre del archivo con el texto de la busceda, facil de hacer
# filtrar objetos que tengan el texto que he inputeado, a si no me da cremas cuando busca old spice
# talvez poder desactivar esto, preguntar un filtar si/no

# anadir lo de time para establecer cuando he encontrado este precio para poder comparar mas tarde


#Use logging or consistent prints to check the flow of execution.
'''
do prints like:
Got firts hidden api
got second hidden api
running data excart with firts api 
'''

