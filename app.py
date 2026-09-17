import streamlit as st
from html import escape

st.set_page_config(
    page_title="GBS — True Cost Per Mile Dashboard",
    page_icon="GBS",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Master demo / URL personalization
# -----------------------------
# One deployed dashboard can be personalized per prospect through URL parameters.
# Example:
# ?company=DEMO&currency=EUR&current=1.92&optimized=1.54&impact=186400
#
# Clients never see editing controls. Each prospect gets a unique URL that opens
# the same master demo with its own prepared-for name and sample figures.

DEFAULTS = {
    "company": "DEMO",
    "currency": "EUR",
    "current": 1.92,
    "optimized": 1.54,
    "impact": 186400,
}

# Country selector: viewers can choose their country and the dashboard
# updates its displayed currency. Values remain illustrative demo figures;
# selecting a currency does not perform a live FX conversion.
COUNTRY_CURRENCIES = {
    '🇦🇫 Afghanistan — AFN (Afghan Afghani)': ('AFN', 'AFN'),
    '🇦🇱 Albania — ALL (Albanian Lek)': ('ALL', 'ALL'),
    '🇩🇿 Algeria — DZD (Algerian Dinar)': ('DZD', 'DZD'),
    '🇦🇸 American Samoa — USD (US Dollar)': ('USD', '$'),
    '🇦🇩 Andorra — EUR (Euro)': ('EUR', '€'),
    '🇦🇴 Angola — AOA (Angolan Kwanza)': ('AOA', 'AOA'),
    '🇦🇮 Anguilla — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇦🇬 Antigua and Barbuda — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇦🇷 Argentina — ARS (Argentine Peso)': ('ARS', 'ARS'),
    '🇦🇲 Armenia — AMD (Armenian Dram)': ('AMD', 'AMD'),
    '🇦🇼 Aruba — AWG (Aruban Florin)': ('AWG', 'AWG'),
    '🇦🇺 Australia — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇦🇹 Austria — EUR (Euro)': ('EUR', '€'),
    '🇦🇿 Azerbaijan — AZN (Azerbaijani Manat)': ('AZN', 'AZN'),
    '🇧🇸 Bahamas — BSD (Bahamian Dollar)': ('BSD', 'BSD'),
    '🇧🇭 Bahrain — BHD (Bahraini Dinar)': ('BHD', 'BHD'),
    '🇧🇩 Bangladesh — BDT (Bangladeshi Taka)': ('BDT', 'BDT'),
    '🇧🇧 Barbados — BBD (Barbadian Dollar)': ('BBD', 'BBD'),
    '🇧🇾 Belarus — BYN (Belarusian Ruble)': ('BYN', 'BYN'),
    '🇧🇪 Belgium — EUR (Euro)': ('EUR', '€'),
    '🇧🇿 Belize — BZD (Belize Dollar)': ('BZD', 'BZD'),
    '🇧🇯 Benin — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇧🇲 Bermuda — BMD (Bermudan Dollar)': ('BMD', 'BMD'),
    '🇧🇹 Bhutan — INR (Indian Rupee)': ('INR', '₹'),
    '🇧🇴 Bolivia, Plurinational State of — BOB (Bolivian Boliviano)': ('BOB', 'BOB'),
    '🇧🇶 Bonaire, Sint Eustatius and Saba — USD (US Dollar)': ('USD', '$'),
    '🇧🇦 Bosnia and Herzegovina — BAM (Bosnia-Herzegovina Convertible Mark)': ('BAM', 'BAM'),
    '🇧🇼 Botswana — BWP (Botswanan Pula)': ('BWP', 'BWP'),
    '🇧🇻 Bouvet Island — NOK (Norwegian Krone)': ('NOK', 'NOK'),
    '🇧🇷 Brazil — BRL (Brazilian Real)': ('BRL', 'R$'),
    '🇮🇴 British Indian Ocean Territory — USD (US Dollar)': ('USD', '$'),
    '🇧🇳 Brunei Darussalam — BND (Brunei Dollar)': ('BND', 'BND'),
    '🇧🇬 Bulgaria — BGN (Bulgarian Lev)': ('BGN', 'BGN'),
    '🇧🇫 Burkina Faso — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇧🇮 Burundi — BIF (Burundian Franc)': ('BIF', 'BIF'),
    '🇨🇻 Cabo Verde — CVE (Cape Verdean Escudo)': ('CVE', 'CVE'),
    '🇰🇭 Cambodia — KHR (Cambodian Riel)': ('KHR', 'KHR'),
    '🇨🇲 Cameroon — XAF (Central African CFA Franc)': ('XAF', 'FCFA'),
    '🇨🇦 Canada — CAD (Canadian Dollar)': ('CAD', 'CA$'),
    '🇰🇾 Cayman Islands — KYD (Cayman Islands Dollar)': ('KYD', 'KYD'),
    '🇨🇫 Central African Republic — XAF (Central African CFA Franc)': ('XAF', 'FCFA'),
    '🇹🇩 Chad — XAF (Central African CFA Franc)': ('XAF', 'FCFA'),
    '🇨🇱 Chile — CLP (Chilean Peso)': ('CLP', 'CLP'),
    '🇨🇳 China — CNY (Chinese Yuan)': ('CNY', 'CN¥'),
    '🇨🇽 Christmas Island — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇨🇨 Cocos (Keeling) Islands — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇨🇴 Colombia — COP (Colombian Peso)': ('COP', 'COP'),
    '🇰🇲 Comoros — KMF (Comorian Franc)': ('KMF', 'KMF'),
    '🇨🇬 Congo — XAF (Central African CFA Franc)': ('XAF', 'FCFA'),
    '🇨🇩 Congo, The Democratic Republic of the — CDF (Congolese Franc)': ('CDF', 'CDF'),
    '🇨🇰 Cook Islands — NZD (New Zealand Dollar)': ('NZD', 'NZ$'),
    '🇨🇷 Costa Rica — CRC (Costa Rican Colón)': ('CRC', 'CRC'),
    '🇭🇷 Croatia — EUR (Euro)': ('EUR', '€'),
    '🇨🇺 Cuba — CUP (Cuban Peso)': ('CUP', 'CUP'),
    '🇨🇼 Curaçao — XCG (Caribbean guilder)': ('XCG', 'Cg.'),
    '🇨🇾 Cyprus — EUR (Euro)': ('EUR', '€'),
    '🇨🇿 Czechia — CZK (Czech Koruna)': ('CZK', 'CZK'),
    "🇨🇮 Côte d'Ivoire — XOF (West African CFA Franc)": ('XOF', 'F\u202fCFA'),
    '🇩🇰 Denmark — DKK (Danish Krone)': ('DKK', 'DKK'),
    '🇩🇯 Djibouti — DJF (Djiboutian Franc)': ('DJF', 'DJF'),
    '🇩🇲 Dominica — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇩🇴 Dominican Republic — DOP (Dominican Peso)': ('DOP', 'DOP'),
    '🇪🇨 Ecuador — USD (US Dollar)': ('USD', '$'),
    '🇪🇬 Egypt — EGP (Egyptian Pound)': ('EGP', 'EGP'),
    '🇸🇻 El Salvador — USD (US Dollar)': ('USD', '$'),
    '🇬🇶 Equatorial Guinea — XAF (Central African CFA Franc)': ('XAF', 'FCFA'),
    '🇪🇷 Eritrea — ERN (Eritrean Nakfa)': ('ERN', 'ERN'),
    '🇪🇪 Estonia — EUR (Euro)': ('EUR', '€'),
    '🇸🇿 Eswatini — SZL (Swazi Lilangeni)': ('SZL', 'SZL'),
    '🇪🇹 Ethiopia — ETB (Ethiopian Birr)': ('ETB', 'ETB'),
    '🇫🇰 Falkland Islands (Malvinas) — FKP (Falkland Islands Pound)': ('FKP', 'FKP'),
    '🇫🇴 Faroe Islands — DKK (Danish Krone)': ('DKK', 'DKK'),
    '🇫🇯 Fiji — FJD (Fijian Dollar)': ('FJD', 'FJD'),
    '🇫🇮 Finland — EUR (Euro)': ('EUR', '€'),
    '🇫🇷 France — EUR (Euro)': ('EUR', '€'),
    '🇬🇫 French Guiana — EUR (Euro)': ('EUR', '€'),
    '🇵🇫 French Polynesia — XPF (CFP Franc)': ('XPF', 'CFPF'),
    '🇹🇫 French Southern Territories — EUR (Euro)': ('EUR', '€'),
    '🇬🇦 Gabon — XAF (Central African CFA Franc)': ('XAF', 'FCFA'),
    '🇬🇲 Gambia — GMD (Gambian Dalasi)': ('GMD', 'GMD'),
    '🇬🇪 Georgia — GEL (Georgian Lari)': ('GEL', 'GEL'),
    '🇩🇪 Germany — EUR (Euro)': ('EUR', '€'),
    '🇬🇭 Ghana — GHS (Ghanaian Cedi)': ('GHS', 'GHS'),
    '🇬🇮 Gibraltar — GIP (Gibraltar Pound)': ('GIP', 'GIP'),
    '🇬🇷 Greece — EUR (Euro)': ('EUR', '€'),
    '🇬🇱 Greenland — DKK (Danish Krone)': ('DKK', 'DKK'),
    '🇬🇩 Grenada — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇬🇵 Guadeloupe — EUR (Euro)': ('EUR', '€'),
    '🇬🇺 Guam — USD (US Dollar)': ('USD', '$'),
    '🇬🇹 Guatemala — GTQ (Guatemalan Quetzal)': ('GTQ', 'GTQ'),
    '🇬🇬 Guernsey — GBP (British Pound)': ('GBP', '£'),
    '🇬🇳 Guinea — GNF (Guinean Franc)': ('GNF', 'GNF'),
    '🇬🇼 Guinea-Bissau — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇬🇾 Guyana — GYD (Guyanaese Dollar)': ('GYD', 'GYD'),
    '🇭🇹 Haiti — HTG (Haitian Gourde)': ('HTG', 'HTG'),
    '🇭🇲 Heard Island and McDonald Islands — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇻🇦 Holy See (Vatican City State) — EUR (Euro)': ('EUR', '€'),
    '🇭🇳 Honduras — HNL (Honduran Lempira)': ('HNL', 'HNL'),
    '🇭🇰 Hong Kong — HKD (Hong Kong Dollar)': ('HKD', 'HK$'),
    '🇭🇺 Hungary — HUF (Hungarian Forint)': ('HUF', 'HUF'),
    '🇮🇸 Iceland — ISK (Icelandic Króna)': ('ISK', 'ISK'),
    '🇮🇳 India — INR (Indian Rupee)': ('INR', '₹'),
    '🇮🇩 Indonesia — IDR (Indonesian Rupiah)': ('IDR', 'IDR'),
    '🇮🇷 Iran, Islamic Republic of — IRR (Iranian Rial)': ('IRR', 'IRR'),
    '🇮🇶 Iraq — IQD (Iraqi Dinar)': ('IQD', 'IQD'),
    '🇮🇪 Ireland — EUR (Euro)': ('EUR', '€'),
    '🇮🇲 Isle of Man — GBP (British Pound)': ('GBP', '£'),
    '🇮🇱 Israel — ILS (Israeli New Shekel)': ('ILS', '₪'),
    '🇮🇹 Italy — EUR (Euro)': ('EUR', '€'),
    '🇯🇲 Jamaica — JMD (Jamaican Dollar)': ('JMD', 'JMD'),
    '🇯🇵 Japan — JPY (Japanese Yen)': ('JPY', '¥'),
    '🇯🇪 Jersey — GBP (British Pound)': ('GBP', '£'),
    '🇯🇴 Jordan — JOD (Jordanian Dinar)': ('JOD', 'JOD'),
    '🇰🇿 Kazakhstan — KZT (Kazakhstani Tenge)': ('KZT', 'KZT'),
    '🇰🇪 Kenya — KES (Kenyan Shilling)': ('KES', 'KES'),
    '🇰🇮 Kiribati — AUD (Australian Dollar)': ('AUD', 'A$'),
    "🇰🇵 Korea, Democratic People's Republic of — KPW (North Korean Won)": ('KPW', 'KPW'),
    '🇰🇷 Korea, Republic of — KRW (South Korean Won)': ('KRW', '₩'),
    '🇰🇼 Kuwait — KWD (Kuwaiti Dinar)': ('KWD', 'KWD'),
    '🇰🇬 Kyrgyzstan — KGS (Kyrgystani Som)': ('KGS', 'KGS'),
    "🇱🇦 Lao People's Democratic Republic — LAK (Laotian Kip)": ('LAK', 'LAK'),
    '🇱🇻 Latvia — EUR (Euro)': ('EUR', '€'),
    '🇱🇧 Lebanon — LBP (Lebanese Pound)': ('LBP', 'LBP'),
    '🇱🇸 Lesotho — ZAR (South African Rand)': ('ZAR', 'ZAR'),
    '🇱🇷 Liberia — LRD (Liberian Dollar)': ('LRD', 'LRD'),
    '🇱🇾 Libya — LYD (Libyan Dinar)': ('LYD', 'LYD'),
    '🇱🇮 Liechtenstein — CHF (Swiss Franc)': ('CHF', 'CHF'),
    '🇱🇹 Lithuania — EUR (Euro)': ('EUR', '€'),
    '🇱🇺 Luxembourg — EUR (Euro)': ('EUR', '€'),
    '🇲🇴 Macao — MOP (Macanese Pataca)': ('MOP', 'MOP'),
    '🇲🇬 Madagascar — MGA (Malagasy Ariary)': ('MGA', 'MGA'),
    '🇲🇼 Malawi — MWK (Malawian Kwacha)': ('MWK', 'MWK'),
    '🇲🇾 Malaysia — MYR (Malaysian Ringgit)': ('MYR', 'MYR'),
    '🇲🇻 Maldives — MVR (Maldivian Rufiyaa)': ('MVR', 'MVR'),
    '🇲🇱 Mali — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇲🇹 Malta — EUR (Euro)': ('EUR', '€'),
    '🇲🇭 Marshall Islands — USD (US Dollar)': ('USD', '$'),
    '🇲🇶 Martinique — EUR (Euro)': ('EUR', '€'),
    '🇲🇷 Mauritania — MRU (Mauritanian Ouguiya)': ('MRU', 'MRU'),
    '🇲🇺 Mauritius — MUR (Mauritian Rupee)': ('MUR', 'MUR'),
    '🇾🇹 Mayotte — EUR (Euro)': ('EUR', '€'),
    '🇲🇽 Mexico — MXN (Mexican Peso)': ('MXN', 'MX$'),
    '🇫🇲 Micronesia, Federated States of — USD (US Dollar)': ('USD', '$'),
    '🇲🇩 Moldova, Republic of — MDL (Moldovan Leu)': ('MDL', 'MDL'),
    '🇲🇨 Monaco — EUR (Euro)': ('EUR', '€'),
    '🇲🇳 Mongolia — MNT (Mongolian Tugrik)': ('MNT', 'MNT'),
    '🇲🇪 Montenegro — EUR (Euro)': ('EUR', '€'),
    '🇲🇸 Montserrat — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇲🇦 Morocco — MAD (Moroccan Dirham)': ('MAD', 'MAD'),
    '🇲🇿 Mozambique — MZN (Mozambican Metical)': ('MZN', 'MZN'),
    '🇲🇲 Myanmar — MMK (Myanmar Kyat)': ('MMK', 'MMK'),
    '🇳🇦 Namibia — ZAR (South African Rand)': ('ZAR', 'ZAR'),
    '🇳🇷 Nauru — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇳🇵 Nepal — NPR (Nepalese Rupee)': ('NPR', 'NPR'),
    '🇳🇱 Netherlands — EUR (Euro)': ('EUR', '€'),
    '🇳🇨 New Caledonia — XPF (CFP Franc)': ('XPF', 'CFPF'),
    '🇳🇿 New Zealand — NZD (New Zealand Dollar)': ('NZD', 'NZ$'),
    '🇳🇮 Nicaragua — NIO (Nicaraguan Córdoba)': ('NIO', 'NIO'),
    '🇳🇪 Niger — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇳🇬 Nigeria — NGN (Nigerian Naira)': ('NGN', 'NGN'),
    '🇳🇺 Niue — NZD (New Zealand Dollar)': ('NZD', 'NZ$'),
    '🇳🇫 Norfolk Island — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇲🇰 North Macedonia — MKD (Macedonian Denar)': ('MKD', 'MKD'),
    '🇲🇵 Northern Mariana Islands — USD (US Dollar)': ('USD', '$'),
    '🇳🇴 Norway — NOK (Norwegian Krone)': ('NOK', 'NOK'),
    '🇴🇲 Oman — OMR (Omani Rial)': ('OMR', 'OMR'),
    '🇵🇰 Pakistan — PKR (Pakistani Rupee)': ('PKR', 'PKR'),
    '🇵🇼 Palau — USD (US Dollar)': ('USD', '$'),
    '🇵🇸 Palestine, State of — ILS (Israeli New Shekel)': ('ILS', '₪'),
    '🇵🇦 Panama — PAB (Panamanian Balboa)': ('PAB', 'PAB'),
    '🇵🇬 Papua New Guinea — PGK (Papua New Guinean Kina)': ('PGK', 'PGK'),
    '🇵🇾 Paraguay — PYG (Paraguayan Guarani)': ('PYG', 'PYG'),
    '🇵🇪 Peru — PEN (Peruvian Sol)': ('PEN', 'PEN'),
    '🇵🇭 Philippines — PHP (Philippine Peso)': ('PHP', '₱'),
    '🇵🇳 Pitcairn — NZD (New Zealand Dollar)': ('NZD', 'NZ$'),
    '🇵🇱 Poland — PLN (Polish Zloty)': ('PLN', 'PLN'),
    '🇵🇹 Portugal — EUR (Euro)': ('EUR', '€'),
    '🇵🇷 Puerto Rico — USD (US Dollar)': ('USD', '$'),
    '🇶🇦 Qatar — QAR (Qatari Riyal)': ('QAR', 'QAR'),
    '🇷🇴 Romania — RON (Romanian Leu)': ('RON', 'RON'),
    '🇷🇺 Russian Federation — RUB (Russian Ruble)': ('RUB', 'RUB'),
    '🇷🇼 Rwanda — RWF (Rwandan Franc)': ('RWF', 'RWF'),
    '🇷🇪 Réunion — EUR (Euro)': ('EUR', '€'),
    '🇧🇱 Saint Barthélemy — EUR (Euro)': ('EUR', '€'),
    '🇸🇭 Saint Helena, Ascension and Tristan da Cunha — SHP (St. Helena Pound)': ('SHP', 'SHP'),
    '🇰🇳 Saint Kitts and Nevis — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇱🇨 Saint Lucia — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇲🇫 Saint Martin (French part) — EUR (Euro)': ('EUR', '€'),
    '🇵🇲 Saint Pierre and Miquelon — EUR (Euro)': ('EUR', '€'),
    '🇻🇨 Saint Vincent and the Grenadines — XCD (East Caribbean Dollar)': ('XCD', 'EC$'),
    '🇼🇸 Samoa — WST (Samoan Tala)': ('WST', 'WST'),
    '🇸🇲 San Marino — EUR (Euro)': ('EUR', '€'),
    '🇸🇹 Sao Tome and Principe — STN (São Tomé & Príncipe Dobra)': ('STN', 'STN'),
    '🇸🇦 Saudi Arabia — SAR (Saudi Riyal)': ('SAR', 'SAR'),
    '🇸🇳 Senegal — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇷🇸 Serbia — RSD (Serbian Dinar)': ('RSD', 'RSD'),
    '🇸🇨 Seychelles — SCR (Seychellois Rupee)': ('SCR', 'SCR'),
    '🇸🇱 Sierra Leone — SLE (Sierra Leonean Leone)': ('SLE', 'SLE'),
    '🇸🇬 Singapore — SGD (Singapore Dollar)': ('SGD', 'SGD'),
    '🇸🇽 Sint Maarten (Dutch part) — XCG (Caribbean guilder)': ('XCG', 'Cg.'),
    '🇸🇰 Slovakia — EUR (Euro)': ('EUR', '€'),
    '🇸🇮 Slovenia — EUR (Euro)': ('EUR', '€'),
    '🇸🇧 Solomon Islands — SBD (Solomon Islands Dollar)': ('SBD', 'SBD'),
    '🇸🇴 Somalia — SOS (Somali Shilling)': ('SOS', 'SOS'),
    '🇿🇦 South Africa — ZAR (South African Rand)': ('ZAR', 'ZAR'),
    '🇬🇸 South Georgia and the South Sandwich Islands — GBP (British Pound)': ('GBP', '£'),
    '🇸🇸 South Sudan — SSP (South Sudanese Pound)': ('SSP', 'SSP'),
    '🇪🇸 Spain — EUR (Euro)': ('EUR', '€'),
    '🇱🇰 Sri Lanka — LKR (Sri Lankan Rupee)': ('LKR', 'LKR'),
    '🇸🇩 Sudan — SDG (Sudanese Pound)': ('SDG', 'SDG'),
    '🇸🇷 Suriname — SRD (Surinamese Dollar)': ('SRD', 'SRD'),
    '🇸🇯 Svalbard and Jan Mayen — NOK (Norwegian Krone)': ('NOK', 'NOK'),
    '🇸🇪 Sweden — SEK (Swedish Krona)': ('SEK', 'SEK'),
    '🇨🇭 Switzerland — CHF (Swiss Franc)': ('CHF', 'CHF'),
    '🇸🇾 Syrian Arab Republic — SYP (Syrian Pound)': ('SYP', 'SYP'),
    '🇹🇼 Taiwan, Province of China — TWD (New Taiwan Dollar)': ('TWD', 'NT$'),
    '🇹🇯 Tajikistan — TJS (Tajikistani Somoni)': ('TJS', 'TJS'),
    '🇹🇿 Tanzania, United Republic of — TZS (Tanzanian Shilling)': ('TZS', 'TZS'),
    '🇹🇭 Thailand — THB (Thai Baht)': ('THB', 'THB'),
    '🇹🇱 Timor-Leste — USD (US Dollar)': ('USD', '$'),
    '🇹🇬 Togo — XOF (West African CFA Franc)': ('XOF', 'F\u202fCFA'),
    '🇹🇰 Tokelau — NZD (New Zealand Dollar)': ('NZD', 'NZ$'),
    '🇹🇴 Tonga — TOP (Tongan Paʻanga)': ('TOP', 'TOP'),
    '🇹🇹 Trinidad and Tobago — TTD (Trinidad & Tobago Dollar)': ('TTD', 'TTD'),
    '🇹🇳 Tunisia — TND (Tunisian Dinar)': ('TND', 'TND'),
    '🇹🇲 Turkmenistan — TMT (Turkmenistani Manat)': ('TMT', 'TMT'),
    '🇹🇨 Turks and Caicos Islands — USD (US Dollar)': ('USD', '$'),
    '🇹🇻 Tuvalu — AUD (Australian Dollar)': ('AUD', 'A$'),
    '🇹🇷 Türkiye — TRY (Turkish Lira)': ('TRY', 'TRY'),
    '🇺🇬 Uganda — UGX (Ugandan Shilling)': ('UGX', 'UGX'),
    '🇺🇦 Ukraine — UAH (Ukrainian Hryvnia)': ('UAH', 'UAH'),
    '🇦🇪 United Arab Emirates — AED (United Arab Emirates Dirham)': ('AED', 'AED'),
    '🇬🇧 United Kingdom — GBP (British Pound)': ('GBP', '£'),
    '🇺🇸 United States — USD (US Dollar)': ('USD', '$'),
    '🇺🇲 United States Minor Outlying Islands — USD (US Dollar)': ('USD', '$'),
    '🇺🇾 Uruguay — UYU (Uruguayan Peso)': ('UYU', 'UYU'),
    '🇺🇿 Uzbekistan — UZS (Uzbekistani Som)': ('UZS', 'UZS'),
    '🇻🇺 Vanuatu — VUV (Vanuatu Vatu)': ('VUV', 'VUV'),
    '🇻🇪 Venezuela, Bolivarian Republic of — VES (Venezuelan Bolívar)': ('VES', 'VES'),
    '🇻🇳 Viet Nam — VND (Vietnamese Dong)': ('VND', '₫'),
    '🇻🇬 Virgin Islands, British — USD (US Dollar)': ('USD', '$'),
    '🇻🇮 Virgin Islands, U.S. — USD (US Dollar)': ('USD', '$'),
    '🇼🇫 Wallis and Futuna — XPF (CFP Franc)': ('XPF', 'CFPF'),
    '🇪🇭 Western Sahara — MAD (Moroccan Dirham)': ('MAD', 'MAD'),
    '🇾🇪 Yemen — YER (Yemeni Rial)': ('YER', 'YER'),
    '🇿🇲 Zambia — ZMW (Zambian Kwacha)': ('ZMW', 'ZMW'),
    '🇿🇼 Zimbabwe — USD (US Dollar)': ('USD', '$'),
    '🇦🇽 Åland Islands — EUR (Euro)': ('EUR', '€'),
}

# Currency symbols accepted in personalized URLs for backward compatibility.
CURRENCY_SYMBOLS = {
    code: symbol for code, symbol in {
        "EUR": "€", "GBP": "£", "USD": "$", "CAD": "C$", "AUD": "A$",
        "CHF": "CHF ", "PLN": "zł", "SEK": "kr", "NOK": "kr", "DKK": "kr",
        "CZK": "Kč", "HUF": "Ft", "RON": "lei", "BGN": "лв", "TRY": "₺",
        "AED": "د.إ", "SAR": "﷼", "INR": "₹", "PKR": "₨", "JPY": "¥",
        "CNY": "¥", "BRL": "R$", "MXN": "MX$", "ZAR": "R", "SGD": "S$",
    }.items()
}

COMPANY_COUNTRIES = {}

params = st.query_params

def _clean_text(value, fallback):
    value = str(value or "").strip()
    return value if value else fallback

def _safe_float(value, fallback, minimum=0.0):
    try:
        number = float(value)
        return number if number >= minimum else fallback
    except (TypeError, ValueError):
        return fallback

def _safe_int(value, fallback, minimum=0):
    try:
        number = int(float(value))
        return number if number >= minimum else fallback
    except (TypeError, ValueError):
        return fallback

prospect_name = _clean_text(params.get("company", DEFAULTS["company"]), DEFAULTS["company"])
requested_currency = _clean_text(params.get("currency", ""), "").upper()
company_country = COMPANY_COUNTRIES.get(prospect_name, "Lithuania")
requested_country = _clean_text(params.get("country", ""), "")

# Prefer a country passed in the personalized URL; otherwise infer it from the prospect.
country_options = list(COUNTRY_CURRENCIES.keys())
def _find_country_label(country_name):
    for label in country_options:
        if label.endswith(f" {country_name} —") or f" {country_name} —" in label:
            return label
    return next((x for x in country_options if company_country in x), country_options[0])

def _find_currency_label(currency_code):
    matches = [x for x in country_options if f"— {currency_code} (" in x]
    return matches[0] if matches else _find_country_label(company_country)

if requested_country:
    selected_country = next((x for x in country_options if x == requested_country), None)
    if selected_country is None:
        selected_country = next((x for x in country_options if requested_country.lower() in x.lower()), None)
    if selected_country is None:
        selected_country = _find_country_label(company_country)
else:
    selected_country = _find_currency_label(requested_currency) if requested_currency else _find_country_label(company_country)

currency_code = COUNTRY_CURRENCIES[selected_country][0]
currency_symbol = COUNTRY_CURRENCIES[selected_country][1]

current_cost = _safe_float(params.get("current", DEFAULTS["current"]), DEFAULTS["current"], 0.01)
optimized_cost = _safe_float(params.get("optimized", DEFAULTS["optimized"]), DEFAULTS["optimized"], 0.01)
annual_impact = _safe_int(params.get("impact", DEFAULTS["impact"]), DEFAULTS["impact"], 0)

# Keep session-state aliases for the existing dashboard calculations.
st.session_state.prospect_name = prospect_name
st.session_state.currency_code = currency_code
st.session_state.currency_symbol = currency_symbol
st.session_state.current_cost = current_cost
st.session_state.optimized_cost = optimized_cost
st.session_state.annual_impact = annual_impact

trucks = [
    ("GBS-104", 1.99),
    ("GBS-107", 1.88),
    ("GBS-102", 1.59),
    ("GBS-101", 1.56),
    ("GBS-103", 1.54),
    ("GBS-105", 1.47),
    ("GBS-108", 1.45),
    ("GBS-106", 1.42),
]

routes = [
    ("Newark, NJ → Columbus, OH", 1.99),
    ("Charlotte, NC → Chicago, IL", 1.88),
    ("LA, CA → Phoenix, AZ", 1.59),
    ("Chicago, IL → Dallas, TX", 1.56),
    ("Atlanta, GA → Miami, FL", 1.54),
    ("Seattle, WA → Denver, CO", 1.47),
    ("Denver, CO → Kansas City, MO", 1.45),
    ("Houston, TX → Memphis, TN", 1.42),
]

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
    :root {
        --bg: #050b13;
        --panel: #0a1420;
        --panel2: #0e1b2a;
        --line: #1d3348;
        --line2: #294963;
        --text: #f5f8fb;
        --muted: #8da1b4;
        --blue: #2f9cf4;
        --cyan: #73d8ff;
        --green: #5bd7a2;
        --red: #ff6b72;
        --yellow: #e8bd57;
    }

    .stApp {
        background:
            radial-gradient(circle at 80% 0%, rgba(35, 112, 174, .12), transparent 25%),
            radial-gradient(circle at 20% 100%, rgba(20, 72, 115, .10), transparent 30%),
            #050b13;
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(5, 11, 19, .98);
        border-bottom: 1px solid rgba(53, 83, 108, .35);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050c15 0%, #07121d 100%);
        border-right: 1px solid #193047;
    }

    [data-testid="stSidebar"] * { color: #e8eff5; }

    .block-container {
        max-width: 1480px;
        padding-top: 1.35rem;
        padding-bottom: 3rem;
    }

    .brand {
        display:flex;
        align-items:center;
        gap:12px;
        margin: 5px 0 27px;
    }

    .brand-logo {
        width:40px;height:40px;border-radius:11px;
        background:linear-gradient(145deg,#2fa8ff,#126fba);
        display:flex;align-items:center;justify-content:center;
        font-weight:900;color:white;font-size:13px;
        box-shadow:0 8px 28px rgba(26,145,224,.22);
        border:1px solid rgba(255,255,255,.10);
    }

    .brand-name {
        font-size:17px;
        line-height:1.05;
        font-weight:800;
        letter-spacing:-.25px;
    }

    .side-foot {
        position: fixed;
        bottom: 18px;
        width: 245px;
        color:#74899c;
        font-size:10px;
        line-height:1.55;
        border-top:1px solid #193047;
        padding-top:13px;
    }

    .topline {
        color:#78b7dc;
        font-size:11px;
        letter-spacing:.55px;
        margin-bottom:17px;
        text-transform:uppercase;
    }

    .warning {
        float:right;
        border:1px solid rgba(221,177,78,.75);
        color:#e9c260;
        border-radius:7px;
        padding:7px 12px;
        font-size:9px;
        letter-spacing:1.05px;
        font-weight:800;
        background:rgba(91,67,17,.10);
    }

    .hero {
        border:1px solid #244159;
        border-radius:15px;
        padding:29px 31px 25px;
        background:
            radial-gradient(circle at 92% 8%, rgba(40,139,215,.17), transparent 28%),
            linear-gradient(145deg,#0d2133 0%,#091521 70%);
        margin-bottom:17px;
        box-shadow:0 18px 55px rgba(0,0,0,.22);
    }

    .hero h1 {
        font-size:36px;
        margin:0 0 7px;
        font-weight:850;
        letter-spacing:-1.35px;
        color:#f7fafc;
    }

    .hero p {
        color:#9eb1c1;
        margin:0;
        font-size:13px;
        line-height:1.55;
    }

    .prepared {
        margin-top:20px;
        display:flex;
        align-items:center;
        gap:12px;
        color:#7f96aa;
        font-size:12px;
    }

    .prospect {
        background:#12263a;
        border:1px solid #31506a;
        color:#f4f8fb;
        border-radius:7px;
        padding:8px 13px;
        font-weight:750;
        box-shadow:inset 0 1px rgba(255,255,255,.035);
    }

    .flow {
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:8px;
        margin-top:22px;
    }

    .flow-item {
        background:rgba(17,38,57,.72);
        border:1px solid #29465f;
        border-radius:8px;
        padding:12px;
        text-align:center;
        font-size:11px;
        color:#dbe7ef;
    }

    .flow-item b { color:#fff; display:block; margin-bottom:3px; }
    .flow-item span { color:#7893a8; font-size:9px; }

    .kpi {
        background:linear-gradient(145deg,#0c1b2a,#091521);
        border:1px solid #263f56;
        border-radius:12px;
        padding:20px;
        min-height:125px;
        box-shadow:0 12px 34px rgba(0,0,0,.16);
    }

    .kpi-label { color:#8da4b7; font-size:11px; letter-spacing:.1px; }
    .kpi-value { color:#f8fafc; font-size:30px; font-weight:850; margin:8px 0 4px; letter-spacing:-.7px; }
    .kpi-sub { color:#6f879b; font-size:10px; }
    .kpi-green .kpi-value { color:#67dfaa; }

    .section-title {
        font-size:13px;
        font-weight:800;
        color:#e9f0f5;
        margin:25px 0 9px;
        letter-spacing:.1px;
    }

    .card {
        background:linear-gradient(145deg,#0b1927,#091520);
        border:1px solid #263f56;
        border-radius:11px;
        padding:18px;
        box-shadow:0 10px 30px rgba(0,0,0,.13);
    }

    .bar-row {
        display:grid;
        grid-template-columns:180px 1fr 55px;
        gap:10px;
        align-items:center;
        margin:9px 0;
        font-size:11px;
    }

    .bar-bg {
        height:8px;
        background:#182c40;
        border-radius:20px;
        overflow:hidden;
    }

    .bar-fill {
        height:100%;
        border-radius:20px;
        background:linear-gradient(90deg,#218ee4,#5bcfff);
        box-shadow:0 0 10px rgba(65,181,245,.16);
    }

    .bar-fill.red { background:#e85d68; box-shadow:none; }
    .bar-fill.green { background:#50ce98; box-shadow:none; }

    .insight {
        border:1px solid #263f56;
        border-radius:9px;
        padding:13px 15px;
        margin:8px 0;
        background:#0b1a29;
        font-size:11px;
        color:#dbe6ee;
    }

    .insight .tag {
        color:#69cfff;
        font-weight:800;
        margin-right:8px;
    }

    .cta {
        background:linear-gradient(120deg,#0d2439,#091725);
        border:1px solid #2b4b66;
        border-radius:11px;
        padding:21px;
        margin-top:20px;
        box-shadow:0 14px 35px rgba(0,0,0,.18);
    }

    .cta h3 { margin:0 0 7px; font-size:18px; }
    .cta p { color:#91a8ba; font-size:11px; margin:0; }

    .footer {
        color:#647c90;
        font-size:9px;
        border-top:1px solid #1b344a;
        padding-top:13px;
        margin-top:28px;
        display:flex;
        justify-content:space-between;
        letter-spacing:.15px;
    }

    .small-note,.page-note {
        color:#70889c;
        font-size:10px;
        margin-bottom:14px;
    }

    .stButton > button {
        background:linear-gradient(135deg,#198fe2,#126eb4);
        color:white;
        border:1px solid rgba(117,211,255,.22);
        border-radius:7px;
        font-weight:800;
        box-shadow:0 7px 20px rgba(20,117,181,.18);
    }

    .stButton > button:hover {
        background:linear-gradient(135deg,#2aa5f4,#1781ca);
        color:white;
        border-color:rgba(117,211,255,.35);
    }

    div[data-baseweb="input"] {
        background:#0e2132;
        border:1px solid #27445c;
        border-radius:7px;
    }

    input { color:white !important; }

    [data-testid="stExpander"] {
        border:1px solid #203a51;
        border-radius:9px;
        background:#091521;
    }

    /* Premium viewer selector */
    div[data-testid="stSelectbox"] {
        max-width: 430px;
        margin-bottom: 10px;
    }

    div[data-testid="stSelectbox"] label {
        color:#8fb1c9 !important;
        font-size:11px !important;
        font-weight:750 !important;
        letter-spacing:.35px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-logo">GBS</div>
        <div class="brand-name">Global Bridge<br>Services</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Cost & Fuel Analytics",
            "Fleet & Routes",
            "Maintenance Tracking",
            "Data Integration",
            "Reports",
        ],
        label_visibility="collapsed",
    )


    st.markdown("""
    <div class="side-foot">
        <b>Demo environment.</b><br>
        All figures are illustrative sample data.<br><br>
        GBS — True Cost Per Mile Dashboard
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Viewer country / currency selector
# -----------------------------
# Client-facing control: visible on the main page, never in the sidebar.
selector_col, spacer_col = st.columns([2.8, 7.2])
with selector_col:
    selected_country = st.selectbox(
        "🌍 Country / Currency",
        options=country_options,
        index=country_options.index(selected_country),
        key="viewer_country",
        help="Select your country. Monetary values on this demo will display using that country's currency.",
    )

# Apply the viewer's choice to every monetary value rendered below.
currency_code, currency_symbol = COUNTRY_CURRENCIES[selected_country]
st.session_state.selected_country = selected_country
st.session_state.currency_code = currency_code
st.session_state.currency_symbol = currency_symbol

# Keep the selection shareable/bookmarkable. Streamlit supports binding widgets to query params.
st.query_params["country"] = selected_country

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="topline">AI-powered logistics analytics, applied to fleet cost '
    '<span class="warning">● ILLUSTRATIVE SAMPLE DATA — NOT ACTUAL CLIENT NUMBERS</span></div>',
    unsafe_allow_html=True
)

# Internal-only helper: open the app with ?admin=1 to see the URL format.
# Normal client links never show this helper.
if str(params.get("admin", "")) == "1":
    with st.expander("GBS Internal — Create a personalized prospect link"):
        st.code(
            f"?company={prospect_name.replace(' ', '%20')}"
            f"&country={selected_country.replace(' ', '%20')}"
            f"&currency={currency_code}"
            f"&current={current_cost:.2f}"
            f"&optimized={optimized_cost:.2f}"
            f"&impact={annual_impact}",
            language="text",
        )
        st.caption("Append this query string to the deployed GBS demo URL. Client-facing links do not show this panel.")

# -----------------------------
# Executive Overview
# -----------------------------
if page == "Executive Overview":
    st.markdown(f"""
    <div class="hero">
        <h1>True Cost Per Mile — By Truck &amp; Route</h1>
        <p>Fuel, driver pay, maintenance, and tolls — unified into one number your ops team<br>
        can act on every morning.</p>
        <div class="prepared">
            <span>Prepared for</span>
            <span class="prospect">{escape(st.session_state.prospect_name)}</span>
        </div>
        <div class="flow">
            <div class="flow-item"><b>Fuel</b><span>Fuel card / purchases</span></div>
            <div class="flow-item"><b>Driver Pay</b><span>Payroll / driver cost</span></div>
            <div class="flow-item"><b>Maintenance</b><span>Service &amp; repairs</span></div>
            <div class="flow-item"><b>Tolls</b><span>Tolls &amp; fees</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">Current fleet average cost per mile</div>
            <div class="kpi-value">{st.session_state.currency_symbol}{st.session_state.current_cost:.2f}<span style="font-size:14px"> / mi</span></div>
            <div class="kpi-sub">Across 8 active trucks · last 30 days · illustrative sample</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        reduction = (1 - st.session_state.optimized_cost / st.session_state.current_cost) * 100
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">Optimized cost / mile</div>
            <div class="kpi-value">{st.session_state.currency_symbol}{st.session_state.optimized_cost:.2f}</div>
            <div class="kpi-sub">↓ {reduction:.0f}% projected improvement</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi kpi-green">
            <div class="kpi-label">Estimated annual impact</div>
            <div class="kpi-value">{st.session_state.currency_symbol}{st.session_state.annual_impact:,.0f}</div>
            <div class="kpi-sub">Projected from flagged inefficiencies</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Current vs. optimized cost</div>', unsafe_allow_html=True)
    a,b,c = st.columns([1,1,1])
    with a:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="kpi-label">Current cost / mile</div>
            <div class="kpi-value">{st.session_state.currency_symbol}{st.session_state.current_cost:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="kpi-label">Optimized cost / mile</div>
            <div class="kpi-value">{st.session_state.currency_symbol}{st.session_state.optimized_cost:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c:
        st.markdown(f"""
        <div class="card" style="text-align:center;border-color:#3f9674">
            <div class="kpi-label">Estimated annual impact</div>
            <div class="kpi-value" style="color:#67dda9">{st.session_state.currency_symbol}{st.session_state.annual_impact:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Where the cost is coming from</div>', unsafe_allow_html=True)
    left,right = st.columns(2)
    with left:
        st.markdown('<div class="card"><b>Cost per mile, by truck</b>', unsafe_allow_html=True)
        maxv = max(v for _,v in trucks)
        for name,val in trucks:
            cls = "red" if val >= 1.88 else ""
            pct = val/maxv*100
            st.markdown(f"""
            <div class="bar-row"><span>{name}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{pct:.1f}%"></div></div>
            <span>{st.session_state.currency_symbol}{val:.2f}</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><b>Cost per mile, by route</b>', unsafe_allow_html=True)
        maxv = max(v for _,v in routes)
        for name,val in routes:
            short = name.replace(" → ", " → ")
            pct = val/maxv*100
            cls = "red" if val >= 1.88 else ""
            st.markdown(f"""
            <div class="bar-row"><span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{short}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{pct:.1f}%"></div></div>
            <span>{st.session_state.currency_symbol}{val:.2f}</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="cta">
        <h3>See what your fleet is actually costing you.</h3>
        <p>Built on your own fuel, payroll, maintenance, and toll data — with a focused view of true cost per mile.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Cost & Fuel Analytics
# -----------------------------
elif page == "Cost & Fuel Analytics":
    st.markdown("## Cost & Fuel Analytics")
    st.markdown('<div class="page-note">Illustrative sample data — use this view to identify where cost-per-mile is coming from.</div>', unsafe_allow_html=True)

    left,right = st.columns(2)
    with left:
        st.markdown('<div class="card"><b>Cost per mile, by truck</b>', unsafe_allow_html=True)
        maxv = max(v for _,v in trucks)
        for name,val in trucks:
            cls = "red" if val >= 1.88 else ""
            st.markdown(f"""
            <div class="bar-row"><span>{name}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{val/maxv*100:.1f}%"></div></div>
            <span>{st.session_state.currency_symbol}{val:.2f}</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><b>Fuel spend composition</b>', unsafe_allow_html=True)
        fuel = [("Diesel purchases",71,""),("Idle-time burn",14,""),("Route detour overhead",9,"red"),("Off-route fuel stops",6,"")]
        for name,val,cls in fuel:
            st.markdown(f"""
            <div class="bar-row"><span>{name}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{val}%"></div></div>
            <span>{val}%</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Cost breakdown — fleet average, per mile</div>', unsafe_allow_html=True)
    components = [("Fuel",.64),("Driver pay",.67),("Maintenance",.29),("Tolls & fees",.10)]
    total = sum(v for _,v in components)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for name,val in components:
        st.markdown(f"""
        <div class="bar-row">
            <span>{name}</span>
            <div class="bar-bg"><div class="bar-fill" style="width:{val/max(v for _,v in components)*100:.1f}%"></div></div>
            <span>{st.session_state.currency_symbol}{val:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Flagged insights</div>', unsafe_allow_html=True)
    for tag,text in [
        ("⚠", "GBS-104 — maintenance cost running 22% above fleet average. Service overdue."),
        ("⛽", "Chicago → Dallas route shows 6% recoverable fuel efficiency vs. benchmark."),
        ("▣", "Projected 12% further savings available through route consolidation on low-utilization lanes."),
    ]:
        st.markdown(f'<div class="insight"><span class="tag">{tag}</span>{text}</div>', unsafe_allow_html=True)

# -----------------------------
# Fleet & Routes
# -----------------------------
elif page == "Fleet & Routes":
    st.markdown("## Fleet & Routes")
    st.markdown('<div class="page-note">Illustrative fleet view. Status flags highlight where attention may be required.</div>', unsafe_allow_html=True)

    rows = [
        ("GBS-101","Chicago, IL → Dallas, TX","88%","On target"),
        ("GBS-102","LA, CA → Phoenix, AZ","91%","On target"),
        ("GBS-104","Newark, NJ → Columbus, OH","62%","Needs attention"),
        ("GBS-106","Houston, TX → Memphis, TN","85%","On target"),
        ("GBS-107","Charlotte, NC → Chicago, IL","78%","Watch"),
    ]

    left,right = st.columns([1.15,1])
    with left:
        st.markdown('<div class="card"><b>Truck / Route / Utilization</b>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:grid;grid-template-columns:90px 1fr 70px 120px;gap:10px;color:#7590a4;font-size:10px;margin:13px 0">
        <span>Truck</span><span>Route</span><span>Utilization</span><span>Status</span></div>
        """, unsafe_allow_html=True)
        for t,r,u,s in rows:
            col = "#57dc9f" if s=="On target" else "#ffd34d" if s=="Watch" else "#ff656d"
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:90px 1fr 70px 120px;gap:10px;
            padding:12px 0;border-top:1px solid #1e354b;font-size:11px">
            <span>{t}</span><span>{r}</span><span>{u}</span><b style="color:{col}">{s}</b></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="card" style="height:100%">
            <b>Route network overview</b>
            <div style="height:260px;position:relative;margin-top:20px">
                <div style="position:absolute;left:12%;bottom:15%;width:12px;height:12px;background:#1da7ff;border-radius:50%"></div>
                <div style="position:absolute;left:34%;bottom:25%;width:12px;height:12px;background:#1da7ff;border-radius:50%"></div>
                <div style="position:absolute;right:20%;top:24%;width:13px;height:13px;background:#53d89a;border-radius:50%"></div>
                <div style="position:absolute;right:10%;bottom:35%;width:13px;height:13px;background:#53d89a;border-radius:50%"></div>
                <svg width="100%" height="100%" style="position:absolute;inset:0">
                    <line x1="17%" y1="78%" x2="80%" y2="31%" stroke="#3a7ea7" stroke-width="2" stroke-dasharray="5 5"/>
                    <line x1="39%" y1="68%" x2="80%" y2="31%" stroke="#3a7ea7" stroke-width="2" stroke-dasharray="5 5"/>
                    <line x1="39%" y1="68%" x2="90%" y2="60%" stroke="#3a7ea7" stroke-width="2" stroke-dasharray="5 5"/>
                </svg>
                <span style="position:absolute;left:8%;bottom:7%;color:#7894a9;font-size:10px">Origin A</span>
                <span style="position:absolute;left:28%;bottom:15%;color:#7894a9;font-size:10px">Origin B</span>
                <span style="position:absolute;right:12%;top:17%;color:#7894a9;font-size:10px">Dest. A</span>
                <span style="position:absolute;right:2%;bottom:27%;color:#7894a9;font-size:10px">Dest. B</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Maintenance
# -----------------------------
elif page == "Maintenance Tracking":
    st.markdown("## Maintenance Tracking")
    st.markdown('<div class="page-note">Illustrative maintenance status and upcoming service view.</div>', unsafe_allow_html=True)
    items = [
        ("⚠", "GBS-104 — service overdue by 9 days. Maintenance cost running 22% above fleet average.", "#ff656d"),
        ("↗", "GBS-107 — brake inspection due in 400 miles.", "#d8e7f2"),
        ("✓", "GBS-101, GBS-102, GBS-106 — up to date, no action needed.", "#55d89a"),
        ("▣", "3 scheduled services in the next 14 days across the fleet.", "#ffd34d"),
    ]
    for icon,text,col in items:
        st.markdown(f"""
        <div class="insight" style="padding:18px">
            <span style="color:{col};font-size:17px;margin-right:13px">{icon}</span>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Data Integration
# -----------------------------
elif page == "Data Integration":
    st.markdown("## Data Integration")
    st.markdown('<div class="page-note">Illustrative source-system connection status.</div>', unsafe_allow_html=True)
    integrations = [
        ("Fuel card provider","Connected",100,"green"),
        ("Dispatch / TMS system","Connected",100,"green"),
        ("Payroll / driver pay","Connected",100,"green"),
        ("Maintenance log system","In progress",62,""),
    ]
    for name,status,pct,cls in integrations:
        st.markdown(f"""
        <div class="card" style="margin-bottom:9px;padding:14px 17px">
            <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px">
                <b>{name}</b><span style="color:{'#58dda0' if status=='Connected' else '#ffd34d'}">{status}</span>
            </div>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{pct}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Reports
# -----------------------------
elif page == "Reports":
    st.markdown("## Reports")
    st.markdown('<div class="page-note">Illustrative report catalogue.</div>', unsafe_allow_html=True)
    reports = [
        "Monthly Cost-per-Mile Summary — PDF, auto-generated on the 1st of each month.",
        "Fleet Efficiency Scorecard — per-truck breakdown, exportable to Excel.",
        "Maintenance Forecast Report — upcoming service needs by vehicle.",
    ]
    for text in reports:
        st.markdown(f'<div class="insight"><span style="color:#d8e7f2;margin-right:12px">□</span>{text}</div>', unsafe_allow_html=True)

# -----------------------------
# Demo controls — kept at the bottom for internal editing
# -----------------------------
# This is intentionally visible so the owner can quickly reuse the same master
# demo for another prospect. It does not create a separate dashboard.
with st.expander("GBS Demo Controls — edit prospect & sample figures", expanded=False):
    ec1, ec2, ec3, ec4 = st.columns([2.2, 1.5, 1.5, 1.6])
    with ec1:
        edit_company = st.text_input(
            "Prepared for",
            value=st.session_state.prospect_name,
            key="edit_prospect_name",
        )
    with ec2:
        edit_current = st.number_input(
            "Current cost / mile",
            value=float(st.session_state.current_cost),
            min_value=0.01,
            step=0.01,
            key="edit_current_cost",
        )
    with ec3:
        edit_optimized = st.number_input(
            "Optimized cost / mile",
            value=float(st.session_state.optimized_cost),
            min_value=0.01,
            step=0.01,
            key="edit_optimized_cost",
        )
    with ec4:
        edit_impact = st.number_input(
            "Annual impact",
            value=int(st.session_state.annual_impact),
            min_value=0,
            step=1000,
            key="edit_annual_impact",
        )

    # Apply edits immediately to the current dashboard and keep them in the
    # URL so the same personalized link can be copied and shared.
    edit_company = _clean_text(edit_company, st.session_state.prospect_name)
    st.session_state.prospect_name = edit_company
    st.session_state.current_cost = float(edit_current)
    st.session_state.optimized_cost = float(edit_optimized)
    st.session_state.annual_impact = int(edit_impact)

    st.query_params["company"] = edit_company
    st.query_params["current"] = f"{edit_current:.2f}"
    st.query_params["optimized"] = f"{edit_optimized:.2f}"
    st.query_params["impact"] = str(int(edit_impact))
    st.caption("Internal editing only. The same master demo can be reused for every prospect; the country/currency selector remains available to the viewer.")

# -----------------------------
# Internal personalization helper
# -----------------------------
# To create a prospect-specific link, add these URL parameters to the deployed app:
# company, currency, current, optimized, impact.
# Example: ?company=DEMO&currency=EUR&current=1.92&optimized=1.54&impact=186400
# The client-facing demo still keeps the country/currency selector; the controls above are for the demo owner.

st.markdown(f"""
<div class="footer">
    <span>Confidential — prepared for {escape(st.session_state.prospect_name)} · Global Bridge Services (GBS)</span>
    <span>INTEGRATE · ANALYZE · OPTIMIZE · GROW</span>
</div>
""", unsafe_allow_html=True)