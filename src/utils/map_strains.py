import pandas as pd
import os


def map_strains(distances):
    # strain names for refseq from csv file
    print('distances', distances)
    curr_path = __file__
    csv_path = os.path.join(os.path.dirname(curr_path), 'data', 'gcf_strain_map.csv')
    df = pd.read_csv(csv_path)
    refseq_ids = [d['sourceid'] for d in distances]
    df = df[df['refseq_id'].isin(refseq_ids)]
    d = dict(zip(df['refseq_id'], df['strain']))
    for i, dist in enumerate(distances):
        if dist['sourceid'] not in d:
            dist['strain'] = None
        else:
            dist['strain'] = d[dist['sourceid']]
        distances[i] = dist
    return distances
