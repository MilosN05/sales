import great_expectations as gx, pandas as pd
import sys
from pathlib import Path

#Provera verzije
print(f"Verzija GX-a: {gx.__version__}")

ucitaj_fajl = "data/product_sales_dataset_final.csv"
if len(sys.argv)==2 and sys.argv[1].endswith(".csv") :
    if Path(f"data/{sys.argv[1]}").exists():
        print(f"Ucitavanje: {sys.argv[1]}")
        ucitaj_fajl=f"data/{sys.argv[1]}"
    else:
        sys.stderr.write(f"Dati {sys.argv[1]} fajl NE POSTOJI u data direktorijumu, pokrecemo {ucitaj_fajl} !\n")



print(f"Fajl za ucitavanje: {ucitaj_fajl}")


#podaci
def izvuci_godinu(str):
    return int(str.split('-')[2])



df = pd.read_csv(ucitaj_fajl)


try:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", format="%m-%d-%y")



    df["Quantity"]=pd.to_numeric(df["Quantity"],errors="coerce")
    df["Unit_Price"]=pd.to_numeric(df["Unit_Price"],errors="coerce")
    df["Revenue"]=pd.to_numeric(df["Revenue"],errors="coerce")
    df["Profit"]=pd.to_numeric(df["Profit"],errors="coerce")


    ##Eventualno dodati u budućnosti
    # df["Customer_Name"] = df["Customer_Name"].str.replace(r"\b(Mr|Mrs|Ms|Miss|Dr)\.?\s*", "", regex=True).str.replace(r"\s+(MD|DVM)$", "", regex=True).str.strip()
    df["City"] = df["City"].str.replace(".", "",regex=False)

    print(df.loc[df["City"].str.contains("St")]["City"].sample(4))

    # titles = ["Mr.", "Mrs.", "Ms.", "Miss", "Dr."]
    # suffixes = ["MD", "DVM","PhD","DDS","Jr."]
    #
    # def otkloni_prefix_suffix(string):
    #     for title in titles:
    #         string=string.replace(title + " ","")
    #
    #
    #
    #     return string
    #
    # df["Customer_Name"]=df["Customer_Name"].apply(otkloni_prefix_suffix)


    df.dropna(how="all", inplace=True)
    # df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True, drop=True)
    df["Order_Year"] = df["Order_Date"].dt.year

except KeyError as ke:
    print(f"Greska, kolone nisu kakve trebaju biti !!! Proveri da nemas neke dodatne slucajne razmake kod naziva kolona !")

#context
context = gx.get_context()

#Spajanje sa poadcima i kreiranje Batch-a
odakle_dolaze_podaci = context.data_sources.add_pandas("pandas")
naziv_podataka = odakle_dolaze_podaci.add_dataframe_asset("sales/prodaja")

sta_je_batch = naziv_podataka.add_batch_definition_whole_dataframe("sales_batch")
batch=sta_je_batch.get_batch(batch_parameters={"dataframe":df})

suite = gx.ExpectationSuite(name="skup_uslova")

#ORDER ID

ne_sme_biti_null = ["Order_ID","Region","Country","City","Product_Name"]
A_Z_Pocetno_veliko = ["Region", "Country","State","City"]

for column in A_Z_Pocetno_veliko:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchRegex(
            column=column,
            regex=r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$"
        )
    )

for column in ne_sme_biti_null:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column=column,

        )
    )


suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Order_ID",
        type_="int64",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="Order_ID"

    )
)

#REGION
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Region",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="Region",
        min_value=2,
        max_value=20

    )
)


#COUNTRY
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Country",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="Country",
        min_value=2,
        max_value=20

    )
)


#Godina
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="Order_Year",
        min_value=2023,
        max_value=2030
    )
)


#Customer Name
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Customer_Name",
        type_="str",


    )
)



suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="Customer_Name",
        min_value=5,
        max_value=40

    )
)



#Grad
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="City",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="City",
        min_value=4,
        max_value=20

    )
)

#State
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="State",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="State",
        min_value=4,
        max_value=20

    )
)


#CATEGORY
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Category",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="Category",
        min_value=4,
        max_value=40

    )
)
#SUB_CATEGORY
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Sub_Category",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="Sub_Category",
        min_value=4,
        max_value=40

    )
)


#PRODUCT_NAME
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Product_Name",
        type_="str",

    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        column="Product_Name",
        min_value=4,
        max_value=50

    )
)


#Quantity

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Quantity",
        type_="int64"
    )
)


suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="Quantity",
        min_value=1,
    )
)

#Unit_Price
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Unit_Price",
        type_="float64"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="Unit_Price",
        min_value=0.0
    )
)





#Revenue
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Revenue",
        type_="float64"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="Revenue",
        min_value=0.0
    )
)


#Profit
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Profit",
        type_="float64"
    )
)




result = batch.validate(suite)

print(result)
print(f"Uspesno: {result.success}" )

if not result.success:
    sys.exit(1)



