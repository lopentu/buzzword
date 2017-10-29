import pandas as pd
import glob
import json
import collections


def recursive_dict():
    return collections.defaultdict(recursive_dict)


def get_relations_after_2016():

    relations_dict = recursive_dict()

    names = ["id", "form", "lemma", "upostag", "xpostag", "feats", "head", "deprel", "deps", "misc"]
    buzzwords = pd.read_table("buzzword/aged.lexicon/target.test.txt", names=["token", "class"])
    pd.options.mode.chained_assignment = None

    for filename in glob.glob("stanford_output/*_raw_after_2016.txt*.conllu"):

        print(filename)

        data = pd.read_table(filename, names=names)

        idx = data.index[(data['id'] == 1) & (~data['form'].isin(['！', '？', '。', '.']))]

        for i in range(0, len(idx) - 1):
            current_post = data[idx[i]:idx[i+1]]

            head_dict = pd.Series(current_post['form'].values, index=current_post['id']).to_dict()

            for index, row in current_post.iterrows():
                if row['head'] != 0:
                    try:
                        head_id = int(row['head'])
                        current_post.loc[index, 'head'] = head_dict[head_id]
                    except:
                        pass

            for index, row in current_post.iterrows():
                if row['head'] in buzzwords['token'].values:
                    buzz = row['head']
                    form = row['form']
                    deprel = row['deprel']

                    if relations_dict[buzz]["token_relations"]:
                        relations_dict[buzz]["token_relations"].append(form)
                    else:
                        relations_dict[buzz]["token_relations"] = [form]

                    if relations_dict[buzz]["syntax_relations"]:
                        relations_dict[buzz]["syntax_relations"].append(deprel)
                    else:
                        relations_dict[buzz]["syntax_relations"] = [deprel]

    with open("after_2016_relations_raw.json", 'w', encoding='utf8') as json_file:
        json.dump(relations_dict, json_file, ensure_ascii=False)

    return relations_dict


def get_relations_before_2016():

    relations_dict = recursive_dict()

    names = ["id", "form", "lemma", "upostag", "xpostag", "feats", "head", "deprel", "deps", "misc"]
    buzzwords = pd.read_table("buzzword/aged.lexicon/target.test.txt", names=["token", "class"])
    pd.options.mode.chained_assignment = None

    for filename in glob.glob("stanford_output/*_raw_before_2016.txt*.conllu"):

        print(filename)

        data = pd.read_table(filename, names=names)

        idx = data.index[(data['id'] == 1) & (~data['form'].isin(['！', '？', '。', '.']))]

        for i in range(0, len(idx) - 1):
            current_post = data[idx[i]:idx[i+1]]

            head_dict = pd.Series(current_post['form'].values, index=current_post['id']).to_dict()

            for index, row in current_post.iterrows():
                if row['head'] != 0:
                    try:
                        head_id = int(row['head'])
                        current_post.loc[index, 'head'] = head_dict[head_id]
                    except:
                        pass

            for index, row in current_post.iterrows():
                if row['head'] in buzzwords['token'].values:
                    buzz = row['head']
                    form = row['form']
                    deprel = row['deprel']

                    if relations_dict[buzz]["token_relations"]:
                        relations_dict[buzz]["token_relations"].append(form)
                    else:
                        relations_dict[buzz]["token_relations"] = [form]

                    if relations_dict[buzz]["syntax_relations"]:
                        relations_dict[buzz]["syntax_relations"].append(deprel)
                    else:
                        relations_dict[buzz]["syntax_relations"] = [deprel]

    with open("before_2016_relations_raw.json", 'w', encoding='utf8') as json_file:
        json.dump(relations_dict, json_file, ensure_ascii=False)

    return relations_dict


def calculate_relations(rel_dict, time):

    calculated_relations = recursive_dict()
    relations_list = []

    for buzz in rel_dict:

        token_relations = rel_dict[buzz]['token_relations']
        syntax_relations = rel_dict[buzz]['syntax_relations']

        relation_tokens = len(token_relations)
        relation_types = len(set(token_relations))
        relations = len(set(syntax_relations))
        relations_formula = relations * (relation_types / relation_tokens)

        calculated_relations[buzz]['relation_tokens'] = relation_tokens
        calculated_relations[buzz]['relation_types'] = relation_types
        calculated_relations[buzz]['relations'] = relations
        calculated_relations[buzz]['relations_formula'] = relations_formula

        relations_list.append({"Buzzword": buzz, "Relation_Formula": relations_formula,
                               "Relation_Types": relation_types, "Relation_Tokens": relation_tokens,
                               "Relations": relations})

    df = pd.DataFrame(relations_list)

    df.to_csv("{}_relations_summary.csv".format(time), encoding='utf8', index=False)

    return calculated_relations, relations_list


if __name__ == "__main__":

    rel_dict_after_2016 = get_relations_after_2016()
    calculate_relations(rel_dict_after_2016, "after_2016")

    rel_dict_before_2016 = get_relations_before_2016()
    calculate_relations(rel_dict_before_2016, "before_2016")
