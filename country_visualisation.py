import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

#Import Company operating sites
txt_amazon="China, Hong Kong, India, Israel, Japan, French Polynesia, Marshall Islands, Micronesia, New Caledonia, New Zealand, Palau, Singapore, South Korea, Puerto Rico, US Virgin Islands, US Minor Outlying Islands, Guam, American Samoa, Northern Mariana Islands, Argentina, Brazil, Costa Rica, Mexico, South Africa, Australia, Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Faroe Islands, Finland, France, Germany, Greece, Greenland, Guernsey, Hungary, Iceland, Ireland, Isle of Man, Italy, Jersey, Latvia, Liechtenstein, Lithuania, Luxembourg, Netherlands, Norway, Poland, Portugal, Russia, San Marino, Slovakia, Slovenia, Spain, Sweden, Switzerland, Turkey, The United Kingdom, United States of America, Canada"
txt_nvda="Argentina, Brazil, Canada, Chile, Colombia, Mexico, Peru, United States, Belgium, Czech Republic, Denmark, Germany, Spain, France, Italy, Netherlands, Norway, Austria, Poland, Romania, Finland, Sweden, Turkey, The United Kingdom,  Australia, Mainland China, India, Japan, Korea, Singapore, Taiwan"
txt_asml="Netherlands, United States, Belgium, France, Germany, Ireland, Israel, Italy, Netherlands, The United Kingdom, China, Japan, Malaysia, Singapore, South Korea, Taiwan"
txt_barrick="United States, Canada, Mali, Côte d'Ivoire, the Democratic Republic of Congo, Tanzania, Papua New Guinea, the Dominican Republic, Argentina, Chile, Zambia, Saudi Arabia, Pakistan"
txt_nio="China, Denmark, Germany, Netherlands, Norway, Sweden, United Arab Emirates, Israel, Azerbaijan"
txt_walmart="United States, Mexico, United Kingdom, China, Canada, South Africa, Chile, Japan, Costa Rica, Guatemala, Honduras, Nicaragua, El Salvador, Argentina, India, Botswana, Zambia, Mozambique, Nigeria, Ghana, Namibia, Lesotho, Kenya, Malawi, Swaziland, Tanzania, Uganda"
txt_xpeng="China, United States, Belgium, Netherlands, Germany, Sweden, Norway"

#Turn into lists
amazon=txt_amazon.split(", ")
nvda=txt_nvda.split(", ")
asml=txt_asml.split(", ")
barrick=txt_barrick.split(", ")
nio=txt_nio.split(", ")
walmart=txt_walmart.split(", ")
xpeng=txt_xpeng.split(", ")

#Add companies to combined dataset
companies = {
    "Amazon": amazon,
    "NVIDIA": nvda,
    "ASML": asml,
    "Barrick": barrick,
    "NIO": nio,
    "Walmart": walmart,
    "XPeng": xpeng,
}

# Load the Natural Earth shapefile
world = gpd.read_file("C:/Users/tumbr/Downloads/data_countries/ne_110m_admin_0_countries.shp")

print("Columns in shapefile:", world.columns)

# Detect which column contains country names
possible_cols = ["ADMIN", "ADMIN_NAME", "NAME", "SOVEREIGNT", "NAME_LONG"]

country_col = None
for col in possible_cols:
    if col in world.columns:
        country_col = col
        break

if country_col is None:
    raise ValueError("Could not find a country-name column!")

print("Using country column:", country_col)

# Rename to standard name
world = world.rename(columns={country_col: "name"})

# Standardize country naming for merging
world["name"] = world["name"].str.replace("United States of America", "United States")
world["name"] = world["name"].str.replace("Côte d'Ivoire", "Ivory Coast")

# Count how many companies operate in each country
from collections import Counter
country_counts = Counter()
for company_list in companies.values():
    for country in company_list:
        country_counts[country] += 1

# Convert to GeoDataFrame
world["count"] = world["name"].map(country_counts).fillna(0)

# Create a custom colormap that starts with white
colors = ['white', '#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15']
n_bins = 100
cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

#Plot
plt.figure(figsize=(20,10))
world.plot(column="count",
           cmap=cmap,
           legend=True,
           edgecolor="black",
           linewidth=0.3,
           vmin=0)  # Ensures 0 maps to white
plt.title("Number of Portfolio Companies Operating in Each Country", fontsize=16)
plt.axis("off")
plt.show()
