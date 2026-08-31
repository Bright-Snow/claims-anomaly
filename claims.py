import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

df = pd.read_csv('medicare_2024.csv')

df = df.rename(columns={
    'Rndrng_NPI': 'npi',
    'Rndrng_Prvdr_Last_Org_Name': 'provider',
    'Rndrng_Prvdr_Type': 'type',
    'HCPCS_Cd': 'code',
    'HCPCS_Desc': 'code_desc',
    'HCPCS_Drug_Ind': 'is_drug',
    'Tot_Srvcs': 'srvcs',
    'Avg_Sbmtd_Chrg': 'charged',
    'Avg_Mdcr_Pymt_Amt': 'paid',
})

def max_gap(s):
    v = s.sort_values().values
    if len(v) < 20 or v[0] <= 0:
        return 1.0
    return (v[1:] / v[:-1]).max()

KEY = ['code', 'type', 'Place_Of_Srvc']

peer = df.groupby(KEY)['paid'].median()
df['peer_median'] = df.set_index(KEY).index.map(peer)
df['peer_ratio'] = df['paid'] / df['peer_median']
df['peer_excess'] = (df['paid'] - df['peer_median']) * df['srvcs']
df['peer_n'] = df.groupby(KEY)['npi'].transform('count')

grp = df.groupby(KEY)['peer_ratio']
df['p90'] = grp.transform(lambda s: s.quantile(0.90))
df['isolation'] = df['peer_ratio'] / df['p90']

df['max_gap'] = df.groupby(KEY)['paid'].transform(max_gap)

# peer baseline: same code, same provider type
peer = df.groupby(['code', 'type'])['paid'].median()

flagged = df[(df['peer_n'] >= 20) & (df['isolation'] >= 1.5) & (df['max_gap'] < 2.0)]

print(flagged.nlargest(15, 'peer_excess')[[
    'provider', 'type', 'code', 'paid', 'peer_median',
    'peer_ratio', 'isolation', 'max_gap', 'srvcs', 'peer_excess'
]])

# providers flagged on more than one distinct code
hits = flagged.groupby('npi').agg(
    provider=('provider', 'first'),
    type=('type', 'first'),
    n_codes=('code', 'nunique'), 
    total_excess=('peer_excess', 'sum'), 
    max_ratio=('peer_ratio', 'max'),
)

repeat = hits[hits['n_codes'] >= 2].sort_values('total_excess', ascending=False)

print(repeat.head(20))

