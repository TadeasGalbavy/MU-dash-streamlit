# App Learning Notes

Tento dokument je ucebna mapa k projektu MU Dash Streamlit. Je pisany v poradi, v akom realne prebieha flow aplikacie: od spustenia Streamlit appky, cez konfiguraciu a nacitanie dat, az po transformacie, KPI, grafy a zobrazenie na jednotlivych strankach.

## 1. Kratky prehlad aplikacie

MU Dash Streamlit je viacstrankovy Streamlit dashboard pre e-commerce/business data. Aktualna verzia sluzi ako bezpecny demo dashboard so sample datami a zaroven ako zaklad pre interny analyticky nastroj, ktory moze neskor citat sukromne firemne data.

Ciel dashboardu je:

- nacitat lokalne CSV alebo Excel subory,
- pripravit z nich analyticke datove modely,
- vypocitat zakladne KPI,
- vytvorit Plotly grafy,
- zobrazit vysledky na Streamlit strankach.

Aplikacia aktualne pouziva hlavne tieto demo data:

- `data/sample/orders.csv`: hlavicky objednavok,
- `data/sample/order_items.csv`: polozky objednavok,
- `data/sample/products.csv`: produktovy ciselnik,
- `data/sample/stock_snapshots.csv`: mesacne skladove snapshoty.

Hlavne casti aplikacie su:

- `app.py`: hlavny vstup do Streamlit aplikacie,
- `pages/*.py`: jednotlive Streamlit stranky,
- `src/config.py`: konfiguracia rezimu a datovych adresarov,
- `src/data_loader.py`: nacitanie CSV/Excel suborov,
- `src/data_validation.py`: technicky sumar DataFrame objektov,
- `src/transformations.py`: priprava analytickych modelov,
- `src/metrics.py`: vypocet KPI,
- `src/charts.py`: tvorba Plotly grafov,
- `scripts/generate_sample_data.py`: generator bezpecnych demo dat,
- `docs/data_schema.md`: popis datovej schemy.

## 2. Flow aplikacie krok za krokom

### Krok 1: Spustenie `app.py`

Aplikacia sa standardne spusta prikazom:

```bash
streamlit run app.py
```

Subor `app.py` nastavi zakladnu Streamlit konfiguraciu cez `st.set_page_config()`, zobrazi hlavny titulok, kratky popis a upozornenie, ze realne firemne data sa nesmu commitovat do GitHubu. Tiez zobrazuje aktualne hodnoty `DATA_MODE` a `DEPLOYMENT_MODE` zo suboru `src/config.py`.

`app.py` sam o sebe nerobi analytiku. Je to vstupna stranka a orientacny bod.

### Krok 2: Konfiguracia datoveho rezimu

Konfiguracia je v `src/config.py`.

Aktualne hodnoty su:

```python
DATA_MODE = "sample"
DEPLOYMENT_MODE = "demo"
```

`DATA_MODE` rozhoduje, odkial sa budu nacitavat data:

- `sample`: cita sa z `data/sample/`,
- `private`: cita sa z `data/private/`.

Tymto sa oddeluje demo rezim od interneho rezimu.

### Krok 3: Nacitanie dat

Nacitanie riesi `src/data_loader.py`.

Stranky ako `pages/01_Overview.py`, `pages/02_Sales.py` a `pages/05_Data_Preview.py` volaju funkcie z data loadera. Loader najprv zisti aktivny datovy adresar a potom nacita podporovane subory.

Podporovane typy su:

- `.csv`,
- `.xlsx`,
- `.xls`.

Hlavny vystup z `load_all_data_files()` je dictionary, kde kluce su nazvy suborov a hodnoty su pandas DataFrame objekty.

Priklad:

```python
{
    "orders.csv": orders_df,
    "order_items.csv": order_items_df,
    "products.csv": products_df,
    "stock_snapshots.csv": stock_snapshots_df,
}
```

### Krok 4: Validacia a technicky preview dat

Validacia v tomto projekte zatial znamena hlavne technicku inspekciu DataFrame objektov. Riesi ju `src/data_validation.py`, ktory obsahuje funkciu `get_dataframe_summary()`.

Ta vracia:

- pocet riadkov,
- pocet stlpcov,
- zoznam stlpcov,
- datove typy,
- pocet chybajucich hodnot.

Pouziva ju stranka `pages/05_Data_Preview.py`. Ta nesluzi na business reporting, ale na rychlu kontrolu, ci su subory nacitane a ako vyzeraju.

### Krok 5: Transformacie

Transformacie su v `src/transformations.py`.

Tu sa surove tabulky menia na analyticke modely. Najdolezitejsia funkcia je:

```python
prepare_orders_model(data)
```

Ta spoji:

```text
order_items.csv
-> orders.csv cez order_id
-> products.csv cez product_id
```

Vystupom je item-level orders model, kde jeden riadok reprezentuje jednu objednanu polozku obohatenu o atributy objednavky a produktu.

Druha dolezita funkcia je:

```python
prepare_latest_stock_snapshot(data)
```

Ta vyberie najnovsi skladovy snapshot a pripoji k nemu produktove atributy.

### Krok 6: KPI a metriky

KPI vypocty su v `src/metrics.py`.

Funkcie dostavaju pripravene DataFrame objekty a vracaju jednoduche hodnoty, napriklad:

- celkovy revenue,
- pocet objednavok,
- predane mnozstvo,
- priemernu hodnotu objednavky,
- pocet aktivnych produktov,
- hodnotu najnovsieho skladu.

Tento subor nepozna Streamlit UI. Jeho ulohou je iba pocitat.

### Krok 7: Grafy

Grafy su v `src/charts.py`.

Funkcie dostavaju pripravene DataFrame objekty a vracaju Plotly `Figure` objekty. Streamlit stranky ich potom zobrazia pomocou:

```python
st.plotly_chart(figure, use_container_width=True)
```

Aktualne grafy pokryvaju:

- revenue over time,
- monthly revenue,
- orders over time,
- revenue by country,
- revenue by category,
- revenue by category donut.

Ak chybaju data alebo potrebne stlpce, chart funkcie vratia prazdny graf s titulkom namiesto toho, aby aplikacia spadla.

### Krok 8: Streamlit stranky

Stranky v `pages/*.py` spajaju vsetko dokopy.

Typicky flow stranky je:

```text
load_all_data_files()
-> prepare_orders_model()
-> volitelne filtre
-> metrics.py
-> charts.py
-> Streamlit UI
```

`pages/01_Overview.py` ukazuje celkovy business prehlad. `pages/02_Sales.py` ukazuje sales pohlad s filtrom krajiny. `pages/05_Data_Preview.py` ukazuje technicky preview nacitanych dat. `pages/03_Stock.py`, `pages/04_Orders.py` a `pages/06_Methodology.py` su zatial placeholdery.

## 3. Subor po subore podla flow

### `app.py`

Sluzba: hlavny vstup do Streamlit aplikacie.

Hlavne funkcie a prvky:

- `st.set_page_config()`,
- `st.title()`,
- `st.write()`,
- `st.warning()`,
- `st.info()`.

Vstupy:

- `DATA_MODE` zo `src/config.py`,
- `DEPLOYMENT_MODE` zo `src/config.py`.

Vystupy:

- uvodna Streamlit stranka,
- informacia o aktualnom rezime.

Nadvazujuce subory:

- `src/config.py`,
- `pages/*.py`, ktore Streamlit zobrazi ako viacstrankovu navigaciu.

Co pochopit ako prve:

- `app.py` nie je miesto, kde sa robi datova logika. Je to uvodna UI vrstva.

### `src/config.py`

Sluzba: centralne miesto pre konfiguraciu projektu.

Hlavne funkcie a konstanty:

- `PROJECT_ROOT`,
- `DATA_MODE`,
- `DEPLOYMENT_MODE`,
- `SAMPLE_DATA_DIR`,
- `PRIVATE_DATA_DIR`,
- `get_configured_data_dir()`.

Vstupy:

- nema runtime vstup od pouzivatela,
- pouziva cestu k aktualnemu suboru na urcenie root adresara projektu.

Vystupy:

- cesty k datovym adresarom,
- informacia, ci sa cita sample alebo private data.

Nadvazujuce subory:

- `app.py`,
- `src/data_loader.py`,
- `pages/05_Data_Preview.py`.

Co pochopit ako prve:

- `DATA_MODE` je hlavny prepinac medzi demo a internym rezimom.

### `src/data_loader.py`

Sluzba: bezpecne nacitanie lokalnych CSV a Excel suborov.

Hlavne funkcie:

- `get_active_data_dir()`,
- `list_data_files()`,
- `load_data_file(file_path)`,
- `load_all_data_files()`,
- `_resolve_safe_data_path(file_path)`.

Vstupy:

- cesta k suboru alebo nazov suboru,
- aktivny datovy adresar podla `DATA_MODE`,
- CSV/XLSX/XLS subory.

Vystupy:

- jeden pandas DataFrame,
- alebo dictionary nazov suboru -> DataFrame.

Nadvazujuce subory:

- `pages/01_Overview.py`,
- `pages/02_Sales.py`,
- `pages/05_Data_Preview.py`,
- `src/transformations.py`.

Co pochopit ako prve:

- Loader len cita data. Nerobi business transformacie.
- `_resolve_safe_data_path()` obmedzuje citanie len na aktivny datovy adresar.

### `src/data_validation.py`

Sluzba: technicky sumar DataFrame objektov.

Hlavna funkcia:

- `get_dataframe_summary(df)`.

Vstupy:

- pandas DataFrame.

Vystupy:

- dictionary s poctom riadkov, poctom stlpcov, stlpcami, datovymi typmi a missing values.

Nadvazujuce subory:

- `pages/05_Data_Preview.py`.

Co pochopit ako prve:

- Toto nie je hlboka business validacia. Je to zakladna inspekcia struktury dat.

### `src/transformations.py`

Sluzba: priprava analytickych datovych modelov zo surovych tabuliek.

Hlavne funkcie:

- `prepare_orders_model(data)`,
- `prepare_latest_stock_snapshot(data)`,
- `_require_files(data, required_files)`.

Vstupy:

- dictionary DataFrame objektov z `load_all_data_files()`.

Vystupy:

- `orders_model`: item-level objednavkovy model,
- `latest_stock`: najnovsi skladovy snapshot obohateny o produktove data.

Nadvazujuce subory:

- `src/metrics.py`,
- `src/charts.py`,
- `pages/01_Overview.py`,
- `pages/02_Sales.py`.

Co pochopit ako prve:

- `prepare_orders_model()` je srdce datoveho flow pre sales a overview.
- Merge logika spaja order items, orders a products.

### `src/metrics.py`

Sluzba: vypocet ciselnych KPI.

Hlavne funkcie:

- `calculate_total_revenue(orders_model)`,
- `calculate_total_orders(orders_model)`,
- `calculate_total_quantity(orders_model)`,
- `calculate_average_order_value(orders_model)`,
- `calculate_active_products(products_df)`,
- `calculate_latest_stock_value(latest_stock_df)`.

Vstupy:

- transformovane DataFrame objekty,
- hlavne `orders_model`, `products_df` a `latest_stock_df`.

Vystupy:

- ciselne hodnoty typu `float` alebo `int`.

Nadvazujuce subory:

- `pages/01_Overview.py`,
- `pages/02_Sales.py`.

Co pochopit ako prve:

- Metriky nepouzivaju Streamlit. Preto sa daju citat ako ciste business pravidla.

### `src/charts.py`

Sluzba: tvorba Plotly grafov.

Hlavne funkcie:

- `create_revenue_over_time_chart(orders_model)`,
- `create_monthly_revenue_chart(orders_model)`,
- `create_orders_over_time_chart(orders_model)`,
- `create_revenue_by_country_chart(orders_model)`,
- `create_revenue_by_category_chart(orders_model)`,
- `create_revenue_by_category_donut_chart(orders_model)`.

Vstupy:

- hlavne `orders_model` alebo jeho filtrovana verzia.

Vystupy:

- Plotly `Figure`.

Nadvazujuce subory:

- `pages/01_Overview.py`,
- `pages/02_Sales.py`.

Co pochopit ako prve:

- Chart funkcia nerenderuje UI. Iba pripravi graf, ktory stranka neskor posle do `st.plotly_chart()`.

### `src/utils.py`

Sluzba: miesto pre buduce zdielane helper funkcie.

Hlavne funkcie:

- aktualne ziadne.

Vstupy:

- aktualne ziadne.

Vystupy:

- aktualne ziadne.

Nadvazujuce subory:

- aktualne ziadne.

Co pochopit ako prve:

- Subor je pripraveny pre buduce utility, ale dnes nie je sucastou aktivneho flow.

### `pages/01_Overview.py`

Sluzba: hlavna business overview stranka.

Hlavne kroky:

- zisti aktivny datovy adresar,
- nacita vsetky data,
- pripravi `orders_model`,
- pripravi `latest_stock`,
- vypocita KPI,
- zobrazi metriky a grafy.

Vstupy:

- data z aktivneho datoveho adresara.

Vystupy:

- KPI cards,
- revenue a orders grafy,
- breakdown grafy podla krajiny a kategorie.

Nadvazujuce subory:

- `src/data_loader.py`,
- `src/transformations.py`,
- `src/metrics.py`,
- `src/charts.py`.

Co pochopit ako prve:

- Toto je najlepsia stranka na pochopenie celeho end-to-end flow.

### `pages/02_Sales.py`

Sluzba: sales analyticka stranka.

Hlavne kroky:

- nacita data,
- pripravi `orders_model`,
- vytvori filter krajiny,
- aplikuje filter na orders model,
- vypocita KPI nad filtrovanou mnozinou,
- zobrazi monthly revenue a category donut chart.

Vstupy:

- data z aktivneho datoveho adresara,
- vyber krajiny zo Streamlit multiselect filtra.

Vystupy:

- filtrovane KPI,
- filtrovane grafy.

Nadvazujuce subory:

- `src/data_loader.py`,
- `src/transformations.py`,
- `src/metrics.py`,
- `src/charts.py`.

Co pochopit ako prve:

- Filter musi menit DataFrame este pred vypoctom metrik a grafov.

### `pages/03_Stock.py`

Sluzba: placeholder pre buducu stock/inventory stranku.

Hlavne funkcie:

- aktualne len Streamlit title a text.

Vstupy:

- ziadne data sa zatial nenacitavaju.

Vystupy:

- placeholder UI.

Nadvazujuce subory:

- zatial ziadne.

Co pochopit ako prve:

- Stranka existuje v navigacii, ale este nema realnu analyticku logiku.

### `pages/04_Orders.py`

Sluzba: placeholder pre buducu order analysis stranku.

Hlavne funkcie:

- aktualne len Streamlit title a text.

Vstupy:

- ziadne data sa zatial nenacitavaju.

Vystupy:

- placeholder UI.

Nadvazujuce subory:

- zatial ziadne.

Co pochopit ako prve:

- Stranka je pripravena pre buduce operacne pohlady na objednavky.

### `pages/05_Data_Preview.py`

Sluzba: technicky nahlad nacitanych dat.

Hlavne kroky:

- zisti aktivny datovy adresar,
- najde podporovane subory,
- nacita kazdy subor,
- zobrazi technicky sumar cez `get_dataframe_summary()`,
- ukaze prvych 10 riadkov.

Vstupy:

- CSV/XLSX/XLS subory z aktivneho adresara.

Vystupy:

- zoznam suborov,
- row/column count,
- dtypes,
- missing values,
- sample riadky.

Nadvazujuce subory:

- `src/data_loader.py`,
- `src/data_validation.py`,
- `src/config.py`.

Co pochopit ako prve:

- Ak nieco nevyzera dobre v data preview, problem je pravdepodobne v zdrojovom subore alebo nacitani.

### `pages/06_Methodology.py`

Sluzba: placeholder pre buducu dokumentaciu vypoctov a datovych pravidiel.

Hlavne funkcie:

- aktualne len Streamlit title a text.

Vstupy:

- ziadne.

Vystupy:

- placeholder UI.

Nadvazujuce subory:

- zatial ziadne.

Co pochopit ako prve:

- Dnes este neobsahuje metodiku. V buducnosti by sem patrili vysvetlenia KPI a business pravidiel.

### `scripts/generate_sample_data.py`

Sluzba: deterministicky generator bezpecnych demo dat.

Hlavne funkcie:

- `generate_products()`,
- `generate_orders()`,
- `generate_order_items(products, orders)`,
- `generate_stock_snapshots(products)`,
- `write_csv(df, file_name)`,
- `main()`.

Vstupy:

- konfiguracne konstanty v subore,
- fixed random seed.

Vystupy:

- CSV subory v `data/sample/`.

Nadvazujuce subory:

- `docs/data_schema.md`,
- `src/data_loader.py`,
- vsetky stranky, ktore citaju sample data.

Co pochopit ako prve:

- Data su fikcne a regenerovatelne. Nemaju reprezentovat realnych zakaznikov, objednavky ani ceny.

### `docs/data_schema.md`

Sluzba: dokumentacia datovej schemy.

Hlavny obsah:

- popis sample suborov,
- popis stlpcov,
- vztahy medzi tabulkami,
- bezpecnostna poznamka.

Vstupy:

- nema programovy vstup.

Vystupy:

- ludska dokumentacia.

Nadvazujuce subory:

- `scripts/generate_sample_data.py`,
- `src/transformations.py`,
- `pages/05_Data_Preview.py`.

Co pochopit ako prve:

- Pred citanim transformacii treba vediet, ake tabulky a kluce existuju.

### `requirements.txt`

Sluzba: zoznam Python zavislosti projektu.

Hlavne polozky:

- `streamlit`,
- `pandas`,
- `openpyxl`,
- `xlrd`,
- `plotly`.

Vstupy:

- pouziva ho `pip install -r requirements.txt`.

Vystupy:

- nainstalovane kniznice potrebne na spustenie aplikacie.

Nadvazujuce subory:

- prakticky cely projekt.

Co pochopit ako prve:

- Bez tychto kniznic sa aplikacia nespusti alebo nebude vediet citat Excel/generovat grafy.

## 4. Datovy tok

Celkovy tok:

```text
data/sample/*.csv alebo Excel
-> data_loader.py
-> data_validation.py
-> transformations.py
-> metrics.py
-> charts.py
-> pages/*.py
-> Streamlit UI
```

### `data/sample/*.csv` alebo Excel

Vstup:

- lokalne CSV/XLSX/XLS subory v aktivnom datovom adresari.

Co sa deje:

- subory fyzicky existuju na disku,
- sample subory su commitnute a bezpecne,
- private subory maju byt lokalne a mimo GitHubu.

Vystup:

- subory pripravene na nacitanie.

Kde hladat chybu:

- ci subor existuje,
- ci je v spravnom adresari,
- ci ma podporovanu priponu,
- ci ma ocakavane nazvy stlpcov.

### `src/data_loader.py`

Vstup:

- aktivny datovy adresar,
- nazvy alebo cesty k datovym suborom.

Co sa deje:

- vyberie sa `data/sample/` alebo `data/private/`,
- najdu sa podporovane subory,
- pandas nacita CSV alebo Excel,
- path safety logika kontroluje, ze subor je priamo v aktivnom adresari.

Vystup:

- DataFrame alebo dictionary DataFrame objektov.

Kde hladat chybu:

- `DATA_MODE`,
- chybajuci adresar,
- nepodporovana pripona,
- chyba pri `pd.read_csv()` alebo `pd.read_excel()`.

### `src/data_validation.py`

Vstup:

- DataFrame nacitany loaderom.

Co sa deje:

- pocitaju sa zakladne technicke vlastnosti DataFrame.

Vystup:

- summary dictionary pre Data Preview stranku.

Kde hladat chybu:

- ak sa preview nezobrazuje, pozri `pages/05_Data_Preview.py`,
- ak su zle stlpce alebo typy, pozri zdrojovy subor a `docs/data_schema.md`.

### `src/transformations.py`

Vstup:

- dictionary DataFrame objektov z `load_all_data_files()`.

Co sa deje:

- overi sa pritomnost povinnych suborov,
- datumy sa konvertuju cez `pd.to_datetime()`,
- tabulky sa spajaju cez `merge()`,
- vyberu sa ocakavane vystupne stlpce.

Vystup:

- `orders_model`,
- `latest_stock`.

Kde hladat chybu:

- chybajuci subor,
- chybajuci join kluc (`order_id`, `product_id`),
- duplikaty v dimenznych tabulkach, ktore by porusili `validate="many_to_one"`,
- chybajuce stlpce ocakavane v `ORDERS_MODEL_COLUMNS`.

### `src/metrics.py`

Vstup:

- transformovane DataFrame objekty.

Co sa deje:

- vybrane stlpce sa konvertuju na cisla,
- pocitaju sa sumy, pocty a priemery,
- prazdne alebo chybajuce data sa vracaju ako nulove hodnoty.

Vystup:

- KPI hodnoty typu `int` alebo `float`.

Kde hladat chybu:

- ci metrika dostava spravny DataFrame,
- ci DataFrame obsahuje potrebny stlpec,
- ci filtrovanie na stranke neodstranilo vsetky riadky.

### `src/charts.py`

Vstup:

- transformovany alebo filtrovany `orders_model`.

Co sa deje:

- data sa agreguju pre konkretny graf,
- datum sa prevadza na mesacny bucket,
- vytvara sa Plotly Express graf,
- pri prazdnych datach sa vracia prazdna `go.Figure`.

Vystup:

- Plotly `Figure`.

Kde hladat chybu:

- chybajuce stlpce,
- zle datove typy datumov,
- prazdny DataFrame po filtroch,
- nespravna agregacia pred grafom.

### `pages/*.py`

Vstup:

- DataFrame objekty,
- KPI hodnoty,
- Plotly Figures,
- pouzivatelske filtre zo Streamlit UI.

Co sa deje:

- stranka vola loader, transformacie, metriky a grafy,
- aplikuje filtre,
- vykresluje texty, metriky, tabulky a grafy.

Vystup:

- Streamlit UI.

Kde hladat chybu:

- poradie volani na stranke,
- ci sa pouziva filtrovany alebo nefiltrovany DataFrame,
- ci stranka spravne zastavi cez `st.stop()` pri chybe,
- ci `st.plotly_chart()` dostava Plotly Figure.

### Streamlit UI

Vstup:

- komponenty definovane v `app.py` a `pages/*.py`.

Co sa deje:

- Streamlit spusti Python skript stranky,
- zobrazi komponenty v browseri,
- pri interakcii pouzivatela stranku znovu prerata.

Vystup:

- interaktivny dashboard.

Kde hladat chybu:

- terminal, kde bezi Streamlit,
- konkretna page file,
- data preview,
- logiku filtrov a stavov prazdnych dat.

## 5. Klucove oblasti, ktore si prejst ako prve

### 1. Nacitanie dat

Preco je dolezite:

- Bez spravneho nacitania neexistuje ziaden dalsi flow.

Subory:

- `src/data_loader.py`,
- `src/config.py`,
- `pages/05_Data_Preview.py`.

Co si vsimnut:

- ako sa vybera aktivny adresar,
- ake pripony su podporovane,
- preco loader obmedzuje cestu na aktivny datovy adresar.

Kontrolna otazka:

- Co presne vrati `load_all_data_files()` a ake maju byt jeho kluce?

### 2. Datova schema

Preco je dolezita:

- Transformacie a metriky predpokladaju konkretne nazvy suborov, stlpcov a vztahov.

Subory:

- `docs/data_schema.md`,
- `data/sample/*.csv`,
- `scripts/generate_sample_data.py`.

Co si vsimnut:

- vztahy cez `order_id` a `product_id`,
- rozdiel medzi order header a order item datami,
- ktore stlpce su business atributy a ktore su technicke kluce.

Kontrolna otazka:

- Preco je revenue v `order_items.csv`, a nie priamo v `orders.csv`?

### 3. Validacia

Preco je dolezita:

- Pomaha rychlo zistit, ci subory vyzeraju tak, ako ocakavas.

Subory:

- `src/data_validation.py`,
- `pages/05_Data_Preview.py`.

Co si vsimnut:

- `get_dataframe_summary()` nerobi business pravidla,
- Data Preview stranka ukazuje strukturu a missing values.

Kontrolna otazka:

- Ako by si cez Data Preview zistil, ze v subore chyba stlpec `product_id`?

### 4. Transformacie

Preco su dolezite:

- Tu vznikaju analyticke DataFrame objekty, z ktorych zije cely dashboard.

Subory:

- `src/transformations.py`,
- `docs/data_schema.md`.

Co si vsimnut:

- `_require_files()`,
- `merge(..., validate="many_to_one")`,
- `ORDERS_MODEL_COLUMNS`,
- konverzia datumov.

Kontrolna otazka:

- Ake tri tabulky sa spoja pri tvorbe `orders_model`?

### 5. Metriky/KPI

Preco su dolezite:

- Su to business cisla, ktore analytik najcastejsie interpretuje.

Subory:

- `src/metrics.py`,
- `pages/01_Overview.py`,
- `pages/02_Sales.py`.

Co si vsimnut:

- metriky dostavaju DataFrame ako vstup,
- vacsina funkcii vracia nulu pri prazdnych alebo chybajucich datach,
- average order value sa rata cez order-level revenue, nie cez priemer riadkov.

Kontrolna otazka:

- Preco `calculate_total_orders()` pouziva `nunique()` nad `order_id`?

### 6. Grafy

Preco su dolezite:

- Grafy su vizualna vrstva nad rovnakymi transformovanymi datami.

Subory:

- `src/charts.py`,
- `pages/01_Overview.py`,
- `pages/02_Sales.py`.

Co si vsimnut:

- chart funkcie vracaju Plotly Figure,
- agregacie sa robia pred volanim Plotly Express,
- prazdne data sa riesia cez `_empty_chart()`.

Kontrolna otazka:

- Kde sa vytvara mesacny stlpec `month` pre revenue grafy?

### 7. Streamlit stranky

Preco su dolezite:

- Tu sa spaja datova logika s pouzivatelskym rozhranim.

Subory:

- `pages/01_Overview.py`,
- `pages/02_Sales.py`,
- `pages/05_Data_Preview.py`,
- `app.py`.

Co si vsimnut:

- poradie volani,
- pouzitie `st.stop()` pri chybach,
- kde sa aplikuju filtre,
- ci metriky a grafy dostavaju filtrovany DataFrame.

Kontrolna otazka:

- Na Sales stranke, co sa stane s KPI, ked vyberies len jednu krajinu?

### 8. Bezpecnost demo vs. private dat

Preco je dolezita:

- Projekt ma byt pouzitelny verejne s demo datami aj lokalne s internymi datami bez rizika commitu sukromnych suborov.

Subory:

- `src/config.py`,
- `src/data_loader.py`,
- `.gitignore`,
- `README.md`,
- `docs/data_schema.md`.

Co si vsimnut:

- `data/sample/` je commitnute,
- `data/private/` je ignorovane,
- `.streamlit/secrets.toml` a `.env` su ignorovane,
- loader cita len z aktivneho datoveho adresara.

Kontrolna otazka:

- Co by sa muselo zmenit, aby aplikacia citala data z `data/private/`?

## 6. Externe kniznice

### Streamlit

Pouzitie:

- tvorba weboveho dashboardu,
- komponenty ako `st.title`, `st.metric`, `st.dataframe`, `st.plotly_chart`, `st.multiselect`.

Kde sa pouziva:

- `app.py`,
- vsetky `pages/*.py`.

Hlba znalost:

- Zatial staci poznat zakladny ucel a najpouzivanejsie komponenty.

### pandas

Pouzitie:

- nacitanie CSV/Excel suborov,
- DataFrame transformacie,
- merge,
- groupby,
- konverzie datumov a cisel,
- sumarizacia missing values.

Kde sa pouziva:

- `src/data_loader.py`,
- `src/data_validation.py`,
- `src/transformations.py`,
- `src/metrics.py`,
- `src/charts.py`,
- `pages/05_Data_Preview.py`,
- `scripts/generate_sample_data.py`.

Hlba znalost:

- Pre datoveho analytika je toto najdolezitejsia kniznica v projekte. Oplati sa poznat ju do vacsej hlbky.

### Plotly

Pouzitie:

- tvorba interaktivnych grafov.

Kde sa pouziva:

- `src/charts.py`.

Hlba znalost:

- Zatial staci rozumiet, ze `plotly.express` rychlo vytvara grafy a vracia `Figure`, ktoru Streamlit zobrazi.

### openpyxl

Pouzitie:

- engine pre citanie `.xlsx` suborov cez pandas.

Kde sa pouziva:

- nepriamo cez `pd.read_excel()` v `src/data_loader.py`.

Hlba znalost:

- Netreba poznat do hlbky. Staci vediet, ze umoznuje nacitat moderne Excel subory.

### xlrd

Pouzitie:

- podpora citania starsich `.xls` suborov cez pandas.

Kde sa pouziva:

- nepriamo cez `pd.read_excel()` v `src/data_loader.py`.

Hlba znalost:

- Netreba poznat do hlbky. Staci poznat jeho ucel.

### pathlib

Pouzitie:

- praca so suborovymi cestami.

Kde sa pouziva:

- `src/config.py`,
- `src/data_loader.py`,
- `scripts/generate_sample_data.py`.

Hlba znalost:

- Je zo standardnej kniznice Pythonu. Staci poznat zaklady `Path`, `resolve()`, `exists()`, `iterdir()`.

### random a datetime

Pouzitie:

- generovanie deterministickych demo dat.

Kde sa pouziva:

- `scripts/generate_sample_data.py`.

Hlba znalost:

- Staci poznat ich ucel v generatore sample dat.

## 7. Bezpecnost dat

Sample data su v:

```text
data/sample/
```

Tieto data su fikcne, bezpecne a commitnute do repozitara.

Private data maju byt v:

```text
data/private/
```

Tieto data nesmu ist na GitHub. Rovnako nesmu ist na GitHub:

- realne zakaznicke data,
- firemne exporty,
- credentials,
- API kluce,
- `.env`,
- `.streamlit/secrets.toml`,
- lokalne ad hoc analyzy s realnymi datami.

Aktualny `.gitignore` chrani:

- `data/private/`,
- `.streamlit/secrets.toml`,
- `.env`,
- `__pycache__/`,
- `*.pyc`,
- `.venv/`,
- `venv/`,
- `.pytest_cache/`,
- `.mypy_cache/`,
- `.ruff_cache/`,
- IDE adresare ako `.idea/` a `.vscode/`.

Aktualna struktura podporuje oddelenie demo a interneho rezimu tym, ze:

- sample data su v `data/sample/`,
- private data maju byt v `data/private/`,
- `DATA_MODE` prepina aktivny zdroj,
- loader cita len z aktivneho datoveho adresara,
- private adresar je ignorovany Gitom.

Co si treba uvedomit:

- Ak sa `DATA_MODE` prepne na `private`, realne subory stale musia zostat lokalne.
- Netreba menit transformacie tak, aby predpokladali iba demo data, pokial ma logika ostat pouzitelna aj pre interny rezim.

## 8. Miesta, ktore mozu byt pre zaciatocnika matuce

### Streamlit spusta stranku od zaciatku pri interakcii

Preco je to matuce:

- Pri zmene filtra Streamlit znova vykona Python skript stranky. Nie je to klasicka web aplikacia s manualnymi callbackmi.

Ako si to prejst:

- Pozri `pages/02_Sales.py` odhora nadol a sleduj, ako sa po vybere krajiny vytvori `filtered_orders_model`.

Minimalne pochopenie:

- Kazda stranka je skript, ktory sa prerata a vykresli aktualny stav UI.

### `load_all_data_files()` vracia dictionary

Preco je to matuce:

- Namiesto jedneho DataFrame vznikne viac DataFrame objektov podla nazvov suborov.

Ako si to prejst:

- Pozri `src/data_loader.py` a potom `src/transformations.py`, kde sa pristupuje k `data["orders.csv"]`.

Minimalne pochopenie:

- Kluc dictionary musi sediet s nazvom suboru, ktory ocakavaju transformacie.

### Item-level orders model

Preco je to matuce:

- Jeden order moze mat viac riadkov, pretoze kazdy riadok je objednana polozka, nie cela objednavka.

Ako si to prejst:

- Porovnaj `orders.csv`, `order_items.csv` a vystup `prepare_orders_model()`.

Minimalne pochopenie:

- Pre revenue je item-level model prirodzeny, ale pocet objednavok treba ratat cez unikatne `order_id`.

### `merge(..., validate="many_to_one")`

Preco je to matuce:

- Pandas validuje, ze prave strany joinu maju pre join kluc najviac jeden zaznam.

Ako si to prejst:

- V `prepare_orders_model()` si vsimni join order items -> orders a order items -> products.

Minimalne pochopenie:

- Viac order item riadkov moze patri jednej objednavke alebo produktu, ale jedna objednavka alebo produkt ma byt v dimenznej tabulke iba raz.

### Prazdne data nehadzu vzdy chybu

Preco je to matuce:

- Niektore funkcie pri prazdnych datach vratia prazdny DataFrame, nulu alebo prazdny graf.

Ako si to prejst:

- Pozri `metrics.py`, `_empty_chart()` v `charts.py` a `st.stop()` v page suboroch.

Minimalne pochopenie:

- Aplikacia sa snazi zobrazit zrozumitelny stav namiesto padu.

### Rozdiel medzi `data_validation.py` a `transformations.py`

Preco je to matuce:

- Oba subory pracuju s datami, ale maju iny ucel.

Ako si to prejst:

- `data_validation.py` cita technicke vlastnosti DataFrame.
- `transformations.py` vytvara business modely.

Minimalne pochopenie:

- Validacia hovori, ako data vyzeraju. Transformacie hovoria, ako sa data pripravia na analyzu.

### `src/utils.py` je prazdny

Preco je to matuce:

- Subor existuje, ale aktualne nie je pouzity.

Ako si to prejst:

- Staci otvorit subor a overit, ze neobsahuje aktivne helpery.

Minimalne pochopenie:

- Netreba ho studovat do hlbky, kym sa don nepridaju zdielane funkcie.

## 9. Mini studijny plan

### Session 1: nacitanie dat a datova schema

Subory citat:

- `README.md`,
- `docs/data_schema.md`,
- `src/config.py`,
- `src/data_loader.py`,
- `pages/05_Data_Preview.py`,
- `data/sample/*.csv`.

Co skusit spustit:

```bash
streamlit run app.py
```

Potom otvor Data Preview stranku a porovnaj zobrazeny obsah so subormi v `data/sample/`.

Otazky:

- Odkial aplikacia cita data v `sample` rezime?
- Ake subory su povinne pre orders model?
- Ake su hlavne join kluce medzi tabulkami?

### Session 2: transformacie a metriky

Subory citat:

- `src/transformations.py`,
- `src/metrics.py`,
- `pages/01_Overview.py`,
- `pages/02_Sales.py`.

Co skusit spustit:

```bash
python scripts/generate_sample_data.py
streamlit run app.py
```

Potom sleduj, ci sa Overview a Sales stranky zobrazia s KPI.

Otazky:

- Ako vznikne `orders_model`?
- Preco sa pocet objednavok nerata ako pocet riadkov?
- Kedy metriky vratia nulu?

### Session 3: grafy a Streamlit stranky

Subory citat:

- `src/charts.py`,
- `pages/01_Overview.py`,
- `pages/02_Sales.py`,
- `pages/03_Stock.py`,
- `pages/04_Orders.py`,
- `pages/06_Methodology.py`.

Co skusit spustit:

```bash
streamlit run app.py
```

Na Sales stranke zmen vyber krajiny a sleduj, ako sa zmenia KPI a grafy.

Otazky:

- Kde sa vytvaraju Plotly Figure objekty?
- Kde sa tieto grafy realne renderuju v Streamlit UI?
- Ktore stranky su hotove analyticke pohlady a ktore su iba placeholdery?

