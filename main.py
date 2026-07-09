import great_expectations as gx, pandas as pd
import sys
from pathlib import Path



# Provera verzije
print(f"Verzija GX-a: {gx.__version__}")
# context
context = gx.get_context(mode="file")

# Spajanje sa poadcima i kreiranje Batch-a
odakle_dolaze_podaci = naziv_podataka=sta_je_batch=suite=validation_definition =None



try:
    odakle_dolaze_podaci=context.data_sources.get("pandas")
    naziv_podataka=odakle_dolaze_podaci.get_asset("salesprodaja")
    sta_je_batch=naziv_podataka.get_batch_definition("salesbatch")
    suite = context.suites.get("skupuslova")
    validation_definition=context.validation_definitions.get("validacija1")
except KeyError as ke:
    odakle_dolaze_podaci = context.data_sources.add_pandas("pandas")
    naziv_podataka = odakle_dolaze_podaci.add_dataframe_asset("salesprodaja")
    sta_je_batch = naziv_podataka.add_batch_definition_whole_dataframe("salesbatch")
    suite = gx.ExpectationSuite(name="skupuslova")
    suite = context.suites.add(suite)

    validation_definition = gx.ValidationDefinition(
        data=sta_je_batch, suite=suite, name="validacija1"
    )


except Exception as ie:
    print(f"Molimo Vas obrisite folder 'gx' i pokrenite ponovo.")
    sys.exit(1)







# ORDER ID

ne_sme_biti_null = ["Order_ID", "Region", "Country", "City", "Product_Name"]
A_Z_Pocetno_veliko = ["Region", "Country", "State", "City"]

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

# REGION
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

# COUNTRY
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

# Godina
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="Order_Year",
        min_value=2023,
        max_value=2030
    )
)

# Customer Name
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

# Grad
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

# State
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

# CATEGORY
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
# SUB_CATEGORY
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

# PRODUCT_NAME
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

# Quantity

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

# Unit_Price
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

# Revenue
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

# Profit
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="Profit",
        type_="float64"
    )
)




# podaci
def izvuci_godinu(str):
    return int(str.split('-')[2])


csv_folder = Path.cwd() / "data"
csv_files = []

for csv_file in csv_folder.iterdir():
    if csv_file.is_file() and csv_file.suffix == ".csv":
        csv_files.append(csv_file)
    else:
        print(f"Svi fajlovi ISKLJUCIVO moraju biti tipa csv, izbaci one koji nisu !")
        sys.exit(1)

for i,csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file)

    try:

        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", format="%m-%d-%y")
        df["Order_ID"] = pd.to_numeric(df["Order_ID"],errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
        df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").astype("float64")
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").astype("float64")
        df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").astype("float64")

        ##Eventualno dodati u budućnosti
        # df["Customer_Name"] = df["Customer_Name"].str.replace(r"\b(Mr|Mrs|Ms|Miss|Dr)\.?\s*", "", regex=True).str.replace(r"\s+(MD|DVM)$", "", regex=True).str.strip()
        df["City"] = df["City"].str.replace(".", "", regex=False)



        df.dropna(how="all", inplace=True)
        df.reset_index(inplace=True, drop=True)
        df["Order_Year"] = df["Order_Date"].dt.year

    except KeyError as ke:
        print(
            f"Greska, kolone nisu kakve trebaju biti !!! Proveri da nemas neke dodatne slucajne razmake kod naziva kolona !")


    batch_parameters_df={"dataframe":df}
    validation_results = validation_definition.run(batch_parameters=batch_parameters_df)
    print(context.get_docs_sites_urls())
    context.build_data_docs()
    if not validation_results.success:
        print(f"Ne uspesan: {csv_file}\n\n")
        print(f"Izvestaj: {validation_results}")
        sys.exit(1)



