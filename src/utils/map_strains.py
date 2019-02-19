import pandas as pd


def map_strains(distances):
    # TODO insert strain names here
    print('distances', distances)
    df = pd.read_csv('data/gcf_strain_map.csv')
    refseq_ids = [d['sourceid'] for d in distances]
    df = df[df['refseq_id'].isin(reseq_ids)]
    d = dict(zip(df['refseq_id'], df['strain']))
    for dist in distances:
        if dist['sourceid'] not in d:
            dist['strain'] = None
        else:
            dist['strain'] = d[dist['sourceid']]
    return distances