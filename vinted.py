# Author : 2$py#5430
# Discord : discord.gg/spyy
# Github : https://github.com/2spy/
# Updated at : 04/07/2022 12:55
# Version : 4.3
# Description : Vinted Bot
# Language : Python
import os
import json
import shutil
import threading
import time
import datetime
import sys
import pytz 
import tzlocal

import multiprocessing

#by pass cloudfare anti-bot
import cloudscraper

try:
    import requests
    from bs4 import BeautifulSoup
except:
    os.system("pip install requests")
    os.system("pip install bs4")

class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[1;0;1m"


def get_info_post(url):
    try:
        time.sleep(2)
        print(f"{Spy.blanc}[{Spy.jaune}RECHERCHE{Spy.blanc}] - Le bot recupere les informations de l'item...")

        # By pass cloudfare scraper
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

        # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        response = scraper.get(url).text  # => "<!DOCTYPE html><html><head>..."
        soup = BeautifulSoup(response, "html.parser")

        # Is it an old item ?
        added_on = soup.findAll('time', {"class": "relative"})
        item_date = added_on[0].attrs["datetime"]
        print("Ajouté le :" + str(item_date))

        # Info items
        res = soup.findAll('script', {"class": "js-react-on-rails-component"})
        descindice = 0
        userinfoindice = 0
        for i in range(len(res)):
            if 'data-component-name="ItemDescription"' in str(res[i]).split():
                descindice = i
            if 'data-component-name="ItemUserInfo"' in str(res[i]).split():
                userinfoindice = i

        description = json.loads(res[descindice].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemDescription" data-dom-id="ItemDescription-react-component-3d79657d-a1b5-4f1d-b501-2f470f328c66" type="application/json">',
            "").replace("</script>", ''))

        userinfo = json.loads(res[userinfoindice].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemUserInfo" data-dom-id="ItemUserInfo-react-component-2105d904-b161-47d1-bfce-9b897a8c1cc6" type="application/json">',
            '').replace("</script>", ''))

        titre = description["content"]["title"]
        description = description["content"]["description"]
        positive = userinfo["user"]["positive_feedback_count"]
        negative = userinfo["user"]["negative_feedback_count"]
        username = userinfo["user"]["login"]
        pays = userinfo["user"]["country_title"]
        ville = userinfo["user"]["city"]

        # check if date of add is greater than bot launching date
        item_add_date = datetime.datetime.strptime(item_date,'%Y-%m-%dT%H:%M:%S%z')
        isNewItem = item_add_date > launching_date_time

        lesinfo = {}

        if titre == "":
            titre = "Pas de donnée"
        if description == "":
            description = "Pas de donnée"
        if positive == "":
            positive = "Pas de donnée"
        if negative == "":
            negative = "Pas de donnée"
        if username == "":
            username = "Pas de donnée"
        if pays == "":
            pays = "Pas de donnée"
        if ville == "":
            ville = "Pas de donnée"
        if item_add_date == "":
            isNewItem = True

        try:
            lesinfo["titre"] = titre
            lesinfo["description"] = description
            lesinfo["positive"] = positive
            lesinfo["negative"] = negative
            lesinfo["username"] = username
            lesinfo["pays"] = pays
            lesinfo["ville"] = ville
            lesinfo["isNewItem"] = isNewItem

        except Exception as err:
            print(err)
        return lesinfo
    except ValueError as err:
        print(f"ValueError {err=}, {type(err)=}")
        pass
    except TypeError as err:
        print(f"TypeError {err=}, {type(err)=}")
        pass
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        pass


def search(url):
    try:
        time.sleep(configs["bot-timing"]["sleep_time_between_requests"])
        print(f"{Spy.blanc}[{Spy.gris}RECHERCHE{Spy.blanc}] - Le bot cherche des nouveaux items...")
        
        # By pass cloudfare scraper
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

        # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        response = scraper.get(url).text  # => "<!DOCTYPE html><html><head>..."

        # Get Random User Agent String.
        '''
        user_agent = user_agent_rotator.get_random_user_agent()

        # Bypass cloudfare protection
        headers.update({'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
        headers.update({'dnt': '1'})

        headers.update({'cookie': 'anon_id=fe294b39-c6ee-49d2-b71c-d3d222a35551; v_udt=dkxwM29uSE5YMDJLT2s3Z3J5Z0lmcm8zODFZS2FhNHJZN0hFeEE9PS0tL2xUT3FJNkhKK0xranh6Ri0tQTNicVNjb1RmdGRIdms5VzhreGxJQT09; v_sid=9c894088d297878fcaa96ed39bb3824e; ab.optOut=This-cookie-will-expire-in-2023; OTAdditionalConsentString=1~39.43.46.55.61.70.83.89.93.108.117.122.124.131.135.136.143.144.147.149.159.162.167.171.192.196.202.211.218.228.230.239.241.259.266.272.286.291.311.317.322.323.326.327.338.367.371.385.389.394.397.407.413.415.424.430.436.445.449.453.482.486.491.494.495.501.503.505.522.523.540.550.559.560.568.574.576.584.587.591.737.745.787.802.803.817.820.821.829.839.864.867.874.899.904.922.931.938.979.981.985.1003.1024.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1127.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1211.1215.1226.1227.1230.1252.1268.1270.1276.1284.1286.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1419.1440.1442.1449.1455.1456.1465.1495.1512.1516.1525.1540.1548.1555.1558.1564.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1665.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2044.2047.2052.2056.2064.2068.2070.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2202.2205.2216.2219.2220.2222.2225.2234.2253.2264.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2394.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2496.2497.2498.2499.2501.2510.2511.2517.2526.2527.2532.2534.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2601.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2634.2636.2642.2643.2645.2646.2647.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2686.2687.2690.2695.2698.2707.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2818.2821.2822.2827.2830.2831.2834.2838.2839.2840.2844.2846.2847.2849.2850.2852.2854.2856.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2911.2912.2913.2914.2916.2917.2918.2919.2920.2922.2923.2924.2927.2929.2930.2931.2939.2940.2941.2947.2949.2950.2956.2961.2962.2963.2964.2965.2966.2968.2970.2973.2974.2975.2979.2980.2981.2983.2985.2986.2987.2991.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3045.3048.3052.3053.3055.3058.3059.3063.3065.3066.3068.3070.3072.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3118.3119.3120.3124.3126.3127.3128.3130.3135.3136.3145.3149.3150.3151.3154.3155.3162.3163.3167.3172.3173.3180.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3197.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3232.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300.3306.3307.3308.3314.3315.3316.3318.3324.3327.3328.3330.3531; domain_selected=true; _gcl_au=1.1.1260718408.1668596238; _lm_id=K3P9C218E0O29XJA; _ga=GA1.1.284118243.1668596238; _ga_ZJHK1N3D75=GS1.1.1668602678.2.1.1668605711.59.0.0; _vinted_fr_session=WXk1Z1lGUVM3a0gySCtGbUhsWXhndk0vL2x6OTFLTTB3ajRkYVJQSjQ1WWx5ZHk3NjBBV3YrUldFYU5YbC9hQnd5bU1Fekp2alhjZjN3b1RLQWhtUm9tWGJISUc2emtJU0RYWk5CNCswcTNST016VjdSd3lkeTRmelVCYWpWdTA5bUh6RjJYeVpTREYwZjJsS2llUGZuU3IyWXp2N2thejVEZHExYmhOYTBsaGp4VlVhbHpJWnU4Sjlabkk3cXdBQzRoaDA2Y1lQaW93aDgxaWdlOFV1VFY4b2NVc1JqcUFEaWM2TkhiZHhWZ0cwR3FBYmJzR0lNQkp2RDFPTDcwNWNhZWk4dUZrMGY5QnZFS3BVM0JGa0R0U3orbVZwMkk0eFczRExCVndwNmRaTjQxalJ1ZkxoNk4xYVNHUDk1dTZDcnV2cDBsUWZkaUdUd3E2VFR4VUZ6Q3VNWUNDOCtIbzUrZ2cxeXh5Y3JJREFkWVZYL3d4TUhFZHR0dXE0MHpWZm5FeUdQa2RxcVluL0VSSFNjaXdTWS9lOWp6bHdwTzR2ak9zaENxV0VYaFJvV2I0di9jQU5BYUF5ZW44UENBRFFvMXdhYWp1UERiNThnbCt2NEhmZ2hsSkZ4Q3BTdWtJeW5RLzNZOXp0ZWtjNnprcUhaTVlXTFRNZTRJZDQ0RUtyUUNITjVwemtSMHJMMEozWENNajF2UXN4ZzlvSExaZzhPS2NveC9PRlpLZ0txckdNcjdrQ2kzcGhqUTVXQitHcWZLNU10NFg2SllNdHN0eDBRUU9jbmdqUUg2QXA1cGU0R0IyWTVzVDF6Mm8xemFyVWlYYkpJWE81OUhZbHg3ZEJmNHVjRnRwYkI5c3pBNTQ5UWpOSG1IVllJa2VtNUlNK1Fqa1lsN29nbFlkK05hU1FoeGJ2SnpqRFBDQTE1a29hNjZTbm9jaTVydHhqejM4cTAxcWdKRXE1bDJUYTdJRHJFdktvVmgvaTMvdlFtRTNDSWVUM0VlbFNWaHZ5VHFYMmpTdFVxZUtmbXVCWi9tNllPZHdXYzBNK0RURk03TjU0VFZNUkFRYlFadnVlL3YyQkZOL2JqWUZ4K0dmVGN0NEdhdDhLbjRBcGhhQnZXS1VWRXQ0V3pXeUcydXdsU2l5M1BTdHZEejFhQlVHR1c4L2NqTUFYeWk3MTBaUldnN3ZxSGUzWk5KcEIwa2RMRWNNbUVYTWg1Mytrb1N1OVdOVlNCZG12ZTQ4aGZXbTQ0YVZQanM5elJmRURCajlXcUtjR1BCbm9RZVJsR3crTWZOMDd0TzZMMExscVpTeHhhV3F1V2VzMWgxekhncFNpNWpCQ0V4YTcwUEZ3ZmYrd2dYTERFS2NZclFxWk9BMWQ3MkRSNDhvVTdreHBWQ1Bsd0xkalh6eEhnaEgzVGE5NWJhcHdFWHVnTUhnY0J0SmpmQTZBd1hSVysySVlrd3owTjkvY2F2TWpnPT0tLTR5cXNmSVYxVXN0alNLY21IUlo1Ync9PQ==--e69f5a12f86afdc7df4a16f8d2c261d56a3db8b1; __cf_bm=c9y64PrtpKNbEYzYGZSj9Jl9sT5GNSk18PYTaB7SaJ0-1668605716-0-AXt1pXAj3Q8TL7KQBDhtajEnOO9aTukC4TGFZwQr0rATfGR0nKMp4F8MdR6qpIibF62Xwt2eP6Zz8A2nCjq2jOzl9KYLw7jSmNHzgAb6Du37Wyenb5zoN/3se9IZY4iNYLe4358KQF0CQk4Meu3sJ3uizU6HOk+ddtZxJ7Oz/WNdKoTJJ3t3OJ4xso9ZTmLTFA==; _dd_s=rum=0&expire=1668606614800; OptanonAlertBoxClosed=2022-11-16T13:35:14.803Z; eupubconsent-v2=CPiiQNgPiiQNgAcABBENCqCsAP_AAAAAAChQJINf_X__b3_r-_59__t0eY1f9_7_v-0zjhfdl-8N2f_X_L8X_2M7vF36pq4KuR4ku3LBIUdlHOHcTUmw6okVryPsbk2cr7NKJ7PEmnMbeydYGH9_n13T-ZKY7___f_77__-____3_____-_f___5____-_f_V__97fn9_____9_P___9v__8_3gAAAAAAAAAD997_AAAAkEAiAAGgAcAB4AJAAoAB_AEWAJEAXwAygBtQDmAOcAdQA-QCDgE_AKGAUsA6oB6AENgIfAR6AkIBIoCVoE2ATaApsBT4CrwFhALiAXKAugBdQC7QF5AMCgYeBiADFgGQgMjAZMA0YBpQDUwGugNoAbcA3QBywDpAHYAOzAd0A8CB5IHlQPdA96B8gHygPsAfuBAQCBgEEQIJgQYAhWBC4CGgSCkAAgABcAFAAVAAyAByADwAQAAwABlADQANQAeQBDAEUAJgAT4AqgCsAFgAN4AcwA9AB-AEJAIYAiQBHQCWAJcATQApQBbgDDAGQAMsAbIA74B7AHxAPsA_YCAAIGARSAi4CMQEaARwAlIBQQCngFXALmAYoA0QBrADaQG4AbwA4gB8gEOgJEATKAnYBQ4CkQFNALFAWgAtgBcgC7wF5gMGAYSAw0BkQDJAGTgMuAZyAz4BpEDWANZAbeA3UBwUDkQOVAcuA8cB7QEIQIXhgDAABgAHABPAEWAOYApYB1AEhAJFAS0AmwBTYC4gGBAMPAZGA10BugDiQHUAOzAdxA90D3gH8BoEIAVgAuACGAGQAMsAbIA7AB-AEAAIKARgAp4BV4C0ALSAawA3gB1QD5AIdARUAkQBOwCkQFyAMJAYwAycBnIDPAGfAOSAcoA_AQAaAAMAA4AEgATwBFgDmAHyAUsA3gCQgEigJaATYAuIBgQDDwGugN0AcSA6gB2YDuIHuge8A-wB_AEGhEBoAKwAhgBkADLAGyAOwAfgBAACMAFPAKuAawA6oB8gEOgJEATsApEBcgDCQGTgM5AZ8A5IBygD8BUBgACgAQwAmABcAEcAMsAdgBHACrwFoAWkA3gCQQFsALkAXmAyIBnIDPAGfANyAckA5QB-AELxQBMAbQA5gB4AEFAKWAdUBHoCRQE2AMCAYfA10DXgG3gOJAe8A-wB_AEDwINjICoAQwAmACOAGWAOwAjgBVwCtgG8AScAtEBbAC8wGRAM5AZ4Az4ByQDlAH4AQvGAFABtADmAHgAUsAsQB1QEegJFATYAvIBgQDDwGugNvAcSA94B8QD7AH8AQbHAbwADAAIgAcAB4AFwASAA5AB-AFAAL4AZAA0AB_AEcAJGAWQBZgC-AGWANqAcwBzgDqAHYAO4AfIBAACCwEHAQgAiIBKgCbQE-AT8ApYBUACsgF6gMAAwIBmQDWAGvAN4AccA6QB1QDyAHoAPkAhABDYCHwERAI9ASEAkUBKwCYgEywJsAm0BQoCkAFJgKYAU2AqYBVQCrwFbAK7AWUAtABagC4gFywLoAuoBgUDDwMQAYsAyEBkwDL4GigaMA0oBpoDU4Guga8A2gBtgDbgHEwOPA5ABzoDpAHWAOwAdmA7UB3ADwIHkgeUA9KB7oHvAPiAfLA-wD7QH4wP2A_gB_oEDwIIgQYAg2BCsCGg6DWAAuACgAKgAZAA5AB8AIAAXQAwADKAGgAagA8AB9AEMARQAmABPgCqAKwAWIAuAC6AGIAMwAbwA5gB6AD9AIYAiYBLAEwAJoAUYApQBYgC3gGEAYcAyADKAGiANkAb4A7wB7QD7AP0Af4BAwCKQEWARgAjgBKQCggFPAKuAWKAtAC0wFzAXUAvIBigDaAG4AOJAdMB1AEOgIqAReAkEBIgCVAEyAJ2AUOApoBVgCxQFsALgAXIAu0Bd4C8wF9AMGAYSAw0BjADHgGSAMnAZUAywBlwDOQGfANEgaQBpIDSwGqgNYAbGA28BuoDi4HJAcqA5cB44D1QHtAPrAfgBAECCQEGgIPAQvIAOgAEABfADQAH8ASIAsgBfADLAG1AOYA5wB2ADwAIKAT4AoYBSwCsgFiAMAAZkA3gB1QDtgHoAQ-Aj0BIQCRYE2ATaAoUBSACkwFtALlAXQAvIBgQDDwGJANFAaUA1MBroDbAG3AOJAdGA7CB5IHlAPRge6B7wD4gH2AP2AgeBBgCDYEKyEDwABYAFAAMgAuABiAEMAJgAUwAqgBcADEAGYAN4AegBHACxAGEAN8Ad4A-wB_gEUAI4ASkAoIBTwCrwFoAWkAuYBigDaAHUASCAkQBJwCVAFNALFAWiAtgBcAC5AF2gMiAZOAzkBngDPgGiANJAaWA1UBwADkgHagPHAfgBBICFAELyQDAAAwADgALgA5AC-AGQASIAsgBcgDLAG0AOYAdwBAACEgE-AKgAVkAzIBrwDeAHVAPsAj0BIoCVgEtQJsAm0BSYCqQFlALlAYeAxYBpQDXQG5AOJAdIA6wB2ADygHvAPsAfuBBECDAENCUDkABAACwAKAAZAA4AB-AGAAYgA8ACIAEwAKoAXAAxABmgEMARIAjgBRgClAFuAMIAbIA7wB-AEcAKeAVeAtAC0gF1AMUAbgA6gB8gEOgIqAReAkQBYoC2AF2gLzAZEAycBlgDOQGeAM-AaQA1gBt4DgAHagPaAfgBA8CCQELwIalAJQABgALgAkAByAD8AKwAXwAyACOAEiALKAXIBfADLAG1AOYA5wB1ADuAHgAPkAgABCQCKgEiAJtAT4BPwChgFLAKyAWIAuoBgADXgG8AOqAdsA8gB6AD_gI9ASKAmIBMsCbAJtAUgApgBTYCnwFTAK7AXKAvIBgQDDwGLAMmAaIA0qBqQGpwNdA14BxIDsAHcAPKge6B7wD4gH2QP2A_cCBgEDwIJgQYAg2BCsCGhSCeAAuACgAKgAZAA5AB8AIIAYABlADQANQAeQBDAEUAJgATwApABVACwAGIAMwAcwA_QCGAIkAUYApQBYgC3AGEAMoAaIA2QB3wD7AP0AiwBGACOAEpAKCAVcArYBcwC8gGKANoAbgBDoCLwEiAJOATsAocBYoC0AFsALgAXIAu0BeYC-gGGgMYAZEAyQBk4DLAGXAM5AZ4Az6BpAGkwNYA1kBsYDbwG6gOCgcmBygDlwHagPHAe0A_ACEIELw.f_gAAAAAAAAA; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+16+2022+14:35:14+GMT+0100+(heure+normale+d’Europe+centrale)&version=202210.1.0&isIABGlobal=false&consentId=fe294b39-c6ee-49d2-b71c-d3d222a35551&hosts=&interactionCount=2&landingPath=NotLandingPage&groups=C0001:1,C0002:1,C0003:1,C0004:1,STACK42:1,C0015:1&geolocation=FR;&AwaitingReconsent=true'.encode('utf-8')})

        headers.update({'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6'})
        headers.update({'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'})

        headers.update({'path': '/vetements?catalog[]=1206&price_from=8&currency=EUR&price_to=20&size_id[]=207&size_id[]=208&size_id[]=209&brand_id[]=53&status[]=6&status[]=1&status[]=2'})
        
        headers.update({'pragma': 'no-cache'})
        headers.update({'sec-ch-ua-mobile': '?0'})
        headers.update({'sec-ch-ua-platform': 'Windows'})
        headers.update({'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"'})
        headers.update({'sec-fetch-dest': 'document'})
        headers.update({'sec-fetch-mode': 'navigate'})
        headers.update({'sec-fetch-site': 'none'})
        headers.update({'sec-fetch-user': '?1'})

        headers.update({'upgrade-insecure-requests': '1'})
        headers.update({'sec-fetch-user': '?1'})

        response = requests.get(str(url), headers=headers)
        if 429 == response.status_code:
            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
            time.sleep(60)
        elif 403 == response.status_code:
            print("403 : request forbidden by Cloudfare firewall")
            print(response.text)
            return
        '''
        soup = BeautifulSoup(response, "html.parser")

        res = soup.findAll('script')
        indices = 0
        for i in range(len(res) + 1):
            if 'data-js-react-on-rails-store="MainStore"' in str(res[i]).split():
                indices += i
                break
        value = res[indices].text.replace('<script z-js-react-on-rails-store="MainStore" type="application/json">', "")
        z = json.loads(value)
        return z
    except Exception as e:
        print("Error in search function: "+repr(e))
        pass

with open("config.json", 'r') as config:
    configs = json.load(config)

try:
    os.system('cls')
except:
    os.system('clear')



asciiart = f"""{Spy.rouge}
██╗   ██╗██████╗  ██████╗ ████████╗
██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║██████╔╝██║   ██║   ██║   
╚██╗ ██╔╝██╔══██╗██║   ██║   ██║   
 ╚████╔╝ ██████╔╝╚██████╔╝   ██║   
  ╚═══╝  ╚═════╝  ╚═════╝    ╚═╝   
         Thx 2$py#5430                     \n\n"""

print(asciiart + "\n\n")

posting = []
#channel = discord.utils.get(server.channels, name="Channel_name_here", type="ChannelType.voice")

local_timezone = tzlocal.get_localzone() # get pytz tzinfo
utc_time = datetime.datetime.utcnow()
launching_date_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

sys.stdout.write("\x1b]2;Vinted Bot\x07")

####################################################
# Main vinted Thread for each Saloon
####################################################
class Moniteur(threading.Thread):

    def __init__(self, webhurl, url, *args, **kwargs):
        super().__init__(target=self, args=args, kwargs=kwargs)
        self._stop = threading.Event()
        self.webhurl = webhurl
        self.url = url        
        pass

    # function using _stop function
    def stop(self):
        self._stop.set()
 
    def stopped(self):
        return self._stop.isSet()

    def run(self, *args, **kwargs):
        # thread kill switch
        while True:
            if self.stopped():
                return
            try:
                z = search(str(self.url))
                x = z["items"]["catalogItems"]["byId"]
                dictlist = list(x)
                for i in range(9, -1, -1):
                    time.sleep(configs["bot-timing"]["sleep_time_item_found"])
                    post = dictlist[i - 1]

                    if str(post) in posting:
                        print(f"{Spy.blanc}[{Spy.rouge}{post}{Spy.blanc}] - Item déjà traité")
                        #time.sleep(configs["bot-timing"]["sleep_time_item_found"])
                        continue
                    else:
                        
                        info = get_info_post(x[str(post)]["url"])
                        
                        # Check if item is new
                        if info["isNewItem"] == False:
                            print(f"{Spy.blanc}[{Spy.rouge}{post}{Spy.blanc}] - Item trop ancien !")
                            posting.append(str(post))
                            continue

                        print(f"{Spy.blanc}[{Spy.vert}{post}{Spy.blanc}] - Nouvel item trouvé !")

                        data = {"username": "$py",
                                "avatar_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024",
                                "embeds": [
                                    {
                                        "description": f"```{configs['embed-color-text']}\n{info['description']}```",
                                        "title": f"``👕`` **__{x[post]['title']}__**",
                                        "color": configs["embed-color"],
                                        "url": x[post]['url'],
                                        "fields": [

                                        ],
                                        "image": {
                                            "url": x[post]["photo"]["thumbnails"][4]["url"]
                                        },
                                        "footer": {
                                            "text": f"つ ◕_◕ ༽つ Merci d'utiliser mes programmes ! <3",
                                            "icon_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024"
                                        }
                                    }]}
                        if configs["embed-config"]["prix"] == "oui":
                            data["embeds"][0]["fields"].append(
                                {
                                    "name": "**``💶`` Prix**",
                                    "value": f"```{configs['embed-color-text']}\n{x[post]['price']}€```",
                                    "inline": True
                                })

                        if configs["embed-config"]["taille"] == "oui":
                            if x[post]['size_title'] == "":
                                size_title = "Pas de donnée"
                            else:
                                size_title = x[post]['size_title']
                            data["embeds"][0]["fields"].append({
                                "name": "**``📏`` Taille**",
                                "value": f"```{configs['embed-color-text']}\n{size_title}```",
                                "inline": True
                            })

                        if configs["embed-config"]["marque"] == "oui":
                            data["embeds"][0]["fields"].append(
                                {
                                    "name": "**``🔖`` Marque**",
                                    "value": f"```{configs['embed-color-text']}\n{x[post]['brand_title']}```",
                                    "inline": True
                                }
                            )

                        if configs["embed-config"]["avis"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "``👍``/``👎`` **Note du vendeur**",
                                "value": f"```{configs['embed-color-text']}\n{str(info['positive'])} - {str(info['negative'])}```",
                                "inline": True
                            })

                        if configs["embed-config"]["localisation"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``📍`` Emplacement **",
                                "value": f"```{configs['embed-color-text']}\n{info['pays']}, {info['ville']}```",
                                "inline": True
                            })

                        if configs["embed-config"]["vendeur"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``👨`` Auteur**",
                                "value": f"```{configs['embed-color-text']}\n{info['username']}```",
                                "inline": True
                            })
                        result = requests.post(self.webhurl, json=data)

                        if 429 == result.status_code:
                            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
                            time.sleep(60)
                        else:
                            posting.append(str(post))
                            print(f"{Spy.blanc}[{Spy.bleu}POSTE{Spy.blanc}] - Poste envoyé !")
            except:
                time.sleep(10)

# Main bot loop
# At each loop : look at sub modifications & load / relaod / stop bot depending on

class SaloonInspector:

    def __init__(self, saloon_name):
        self.name= saloon_name
        self.vinted_thread = []
        self.web_url = []
        self.is_alive = False

#######
# Main function
#######
Saloons = dict()
while True:

    with open("config.json", 'r') as config:
        configs = json.load(config)

    # Reset all is_alive properties
    for saloon in Saloons.values():
        saloon.is_alive = False

    #TODO :  Move this "if" elsewhere
    if len(configs["suburl"]) > configs["bot-timing"]["max_thread_numbers"]:
        print(
            f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Trop de salon veuillez en enlever car le bot se fera rate limit !")
    else:

        for webhurl in configs["suburl"]:

            saloon_name = configs['suburl'][webhurl]['salon']
            saloon_name = saloon_name.encode('utf-8', 'ignore')

            print(
                f"{Spy.blanc}[{Spy.violet}LANCEMENT{Spy.blanc}] - Lancement de la tâche dans le salon {Spy.jaune}{configs['suburl'][webhurl]['salon']}")

            url = configs["suburl"][str(webhurl)]["url"]

            if saloon_name in Saloons:
                saloon_inspector = Saloons[saloon_name]
                if saloon_inspector.web_url != webhurl :
                    saloon_inspector.vinted_thread.stop()
                    saloon_inspector.vinted_thread = Moniteur(webhurl=webhurl, url=url, args=[webhurl, url])
                    saloon_inspector.vinted_thread.start()

                # Saloon found : keep it alive
                saloon_inspector.is_alive = True
            else:

                # add a new thread for this salon
                saloon_inspector = SaloonInspector(saloon_name)
                saloon_inspector.vinted_thread =Moniteur(webhurl=webhurl, url=url, args=[webhurl, url])
                #saloon_inspector.vinted_thread = multiprocessing.Process(target=moniteur, args=[webhurl, configs["suburl"][str(webhurl)]["url"]])
                saloon_inspector.web_url = webhurl
                saloon_inspector.is_alive = True
                saloon_inspector.vinted_thread.start()

                Saloons[saloon_name] = saloon_inspector

        # Remove useless thread for deleted saloon url
        for saloon in list(Saloons.items()):
            if saloon[1].is_alive == False:
                print("Arret du salon : " + str(saloon[0]))
                saloon[1].vinted_thread.stop()
                del Saloons[saloon[0]]

    time.sleep(30)
