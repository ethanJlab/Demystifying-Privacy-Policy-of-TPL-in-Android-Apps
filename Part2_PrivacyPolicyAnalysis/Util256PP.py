# -*- coding:utf-8 -*-
# Author: Kaifa Zachary ZHAO
# Date: 11/1/2021
import os
import codecs
import re
import hanlp
import phrasetree
from hanlp.components.mtl.tasks.tok.tag_tok import TaggingTokenization



collectWords = ["收集", "获取", "接受", "接收", "保存",
                "使用", "采集", "记录", "存储"]
sharingWords = ["披露", "分享", "共享", "交换",
                "报告", "公布", "发送", "交换", "转移", "迁移",
                "转让", "公开", "透露", "提供"]
NOT_DATA = ["信息", "此信息", "这类信息", "相关信息", "上述信息",
            "其他信息", "前述信息", "该信息", "上述功能", "以上信息",
            "服务", "产品", "性能", "这些信息", "公司", "合同",
            "用户", "本产品", "我们的产品", "一些功能", "票根", "软件开发工具包（SDK）",
            "相关特定功能", "功能", "情形", "行为", "人士", "网站", "访问", "比赛或促销活动", "者", "修改、替代、升级",
            "替代", "强国", "注", "电子银行", "强国", "学习平台", "用途和目的", "BUG", "Cookie", "Cookies", "cookie", "cookies",
            "具体服务", "这类服务", "我们的服务", "高考圈", "公开或共用户方", "未成年人", "订单", "墨墨", "注",
            "我们", "您的权益", "原因", "数据", "更新", "活动", "到站时间和距离", "统一的注册和登录",
            "合法性", "配合", "司法", "配合", "协助", "司法", "商标", "商业", "知识产权或权利", "标识", "著作权和/或商标权", "“爱豆”",
            "范围", "方式", "组织", "下列与您有关的信息", "目的", "各种安全技术和程序", "软件工具开发包", "我们", "产品与/或服务",
            "诸葛万年历", "登陆", "为您提供服务所需"]


def extract_soc_pattern(sentence_list, HanLP_MTM, crf):
    ded_set = []
    sen_set = []
    for sen in sentence_list:
        # 去除 “如何” “ 原则上”等
        if "如何" in sen or "原则" in sen:
            continue
        # remove unicode characters
        raw_sen = sen
        pattern = re.compile(r'[\uf001-\uf0ff]')
        sen = re.sub(pattern, "", sen).strip()
        try:
            han_results = HanLP_MTM(sen)
        except Exception:
            print("\t cannot be handled by hanlp")
            continue
        if len(han_results.keys()) == 0:
            continue

        ner_label = crf.identify_sentence(han_results["tok/fine"], han_results['pos/ctb'])
        if len(ner_label) == 0:
            continue
        if check_pattern(sen):
            continue

        # if "用服务时我们可能收集已经经" in sen:
        #     aaa = 1

        temp = extract_parsetree(han_results, ner_label[0]["ner"])
        temp = post_process_soc(temp)
        ded_set.extend(temp)
        for cz in range(len(temp)):
            sen_set.append(raw_sen)
    return ded_set, sen_set


def post_process_soc(raw_soc):
    new_soc = []
    for idx, soc in enumerate(raw_soc):
        data = soc[2]
        tmp_idx = []
        # tt
        for i, d in enumerate(data):
            if d.startswith("您"):
                data[i] = d.replace("您", "")
            if d.startswith("您的"):
                data[i] = d.replace("您的", "")
            if "/" in d:
                data.extend(d.split("/"))
                tmp_idx.append(i)
                # data.remove(d)
            elif "、" in d:
                data.extend(d.split("、"))
                tmp_idx.append(i)
                # data.remove(d)
            if not check_data(d):
                tmp_idx.append(i)
        for ziiii in tmp_idx[::-1]:
            data.pop(ziiii)
        soc[2] = list(set(data))
        soc[1] = list(set(soc[1]))

        # for
        if len(data) == 1 and len(data[0]) < 2:
            raw_soc.pop(idx)
            continue
        new_soc.append(soc)
        if len(data) == 0:
            return []
    return new_soc


def token_list_to_dep_info(tokenResult, depResult):
    depInfoWords = []
    for tokenIndex in range(1, len(tokenResult) + 1):
        depWord = tokenResult[tokenIndex - 1]
        depInfo = depResult[tokenIndex - 1]
        govWordIndex = depInfo[0]
        govWord = tokenResult[govWordIndex - 1]
        rel = depInfo[1]
        # print(tokenIndex, depWord, '<-%s-' % rel, govWordIndex, govWord)
        depInfoWords.append([rel, govWordIndex, govWord, tokenIndex, depWord])
    return depInfoWords


def extract_parsetree(hanlp_results: dict, ner_label):
    hanlp_token = hanlp_results["tok/fine"]
    hanlp_dep = hanlp_results["dep"]
    hanlp_ptree = hanlp_results["con"]
    hanlp_pos = hanlp_results["pos/ctb"]
    wordDepInfo = token_list_to_dep_info(hanlp_token, hanlp_dep)
    # merger noun phase
    token = hanlp_token.copy()
    token = noun_merge_tree_based(token, hanlp_ptree, hanlp_results)
    verb_flag = [0 for i in token]
    DED = []
    # 用于记录长句第二单词开始的位置
    beg_flag = 0
    # label SoC verb
    for i in range(len(hanlp_token)):
        # pos is verb and in SoC list
        if hanlp_pos[i] == "VV":
            verb = hanlp_token[i]
            if (verb in sharingWords or verb in collectWords) and verb_flag[i] != 1:
                actor, action, data, entity, neg = [], [verb], [], [], []
                root_verb_idx = i
                verb_flag[i] = 1
                if verb == "提供" and token[i - 1] in ["您", "用户"]:
                    actor.append("您")
                if i < beg_flag and beg_flag != 0:
                    beg_flag = 0
                    for bf in range(i, -1, -1):
                        if token[bf] in [";", "；", "。", "，"]:
                            beg_flag = bf + 1
                            break
                data = extract_dataobj_from_tree(tar_verb_idx=i, han_results=hanlp_results)
                if len(data) == 0 or (not check_data(data)):
                    continue

                for s_idx in range(beg_flag, len(wordDepInfo)):
                    # get actor and entity by "nsubj" and "dobj"
                    sactor = wordDepInfo[s_idx]
                    cur_tok = token[s_idx]
                    # sentence break
                    if cur_tok in [";", "；", "。"]:
                        if s_idx < i:
                            continue
                        # if len(data) == 1 and (not checkData(data[0])):
                        #     data = []
                        if not check_data(data):
                            data = []
                        tt = [len(t) for t in [actor, action, data, entity, neg]]
                        if tt.count(0) < 4:
                            if (not check_data(data)) or len(data) == 0:
                                continue
                            if len(data) == 1 and (not check_data(data)):
                                continue
                            data = list(set(data))
                            actor = list(set(actor))
                            DED.append([actor, action, data, entity, neg])
                        actor, action, data, entity, neg = [], [], [], [], []
                        beg_flag = s_idx + 1
                        break

                    if is_chinese_or_punct(cur_tok) or sactor[0] == "punct":
                        continue

                    ##
                    if sactor[1] - 1 == root_verb_idx:
                        # if not check_data(cur_tok):
                        #     continue
                        if sactor[0] == "nsubj":
                            # if "信息" in cur_tok or ner_label[s_idx] == "dataObj":
                            # if ner_label[s_idx] == "dataObj":
                            #     data.extend([cur_tok])
                            # else:
                            actor.append(cur_tok)
                        elif sactor[0] == "pobj":
                            if not check_data(cur_tok):
                                continue
                            entity.append(cur_tok)
                        elif cur_tok in ["我", "我们", "你", "你们", "您"]:
                            actor.append(cur_tok)
                        elif sactor[0] == 'advmod' or sactor[0] == 'mmod':
                            if cur_tok in ["不", "不会", "不允许", "不能", "没有"]:
                                neg.append("不")
                            if cur_tok == "如果":
                                actor = []
                                action = []
                                data = []
                                entity = []
                                neg = []
                                beg_flag = s_idx + 1
                                break
                        elif sactor[0] == "neg":
                            neg.append(cur_tok)
                        elif sactor[0] == "dep" or sactor[0] == "conj":
                            # 并列动词
                            if cur_tok in collectWords or cur_tok in sharingWords:
                                action.append(cur_tok)
                                data.extend(extract_dataobj_from_tree(tar_verb_idx=s_idx, han_results=hanlp_results))
                                verb_flag[s_idx] = 1
                    elif sactor[3] - 1 == root_verb_idx:
                        # 到该词本身
                        if sactor[0] == "pccomp" or sactor[0] == "conj" or sactor[0] == "ccomp":
                            if sactor[2] == sactor[-1]:
                                continue
                            # 介词补语情况，找到主语 or 并列动词情况，找到主语
                            if hanlp_pos[sactor[1] - 1] == "VV":
                                tmp_actor = get_pccomp_subj(wordDepInfo, s_idx, hanlp_pos, token)
                                actor.extend(tmp_actor)
                        elif sactor[0] == "dep" and sactor[2] in ["不", "不会", "不允许", "无法"]:
                            # 处理类似："X 不允许 Y 收集/分享 data”的pattern
                            neg.append("不")
                            tar_idx = sactor[1] - 1
                            for ti in range(tar_idx + 1, s_idx):
                                if wordDepInfo[ti][1] - 1 == tar_idx and wordDepInfo[ti][0] == "dobj":
                                    actor.append(token[wordDepInfo[ti][-2] - 1])
                        elif sactor[0] == "dep":
                            if sactor[2] == sactor[-1]:
                                continue
                            tar_idx = sactor[1] - 1
                            # for ti in range(tar_idx + 1, s_idx):
                            #     if wordDepInfo[ti][1] - 1 == tar_idx and wordDepInfo[ti][0] == "dobj":
                            #         actor.append(token[wordDepInfo[ti][-2] - 1])
                            for ti in range(s_idx, -1, -1):
                                if wordDepInfo[ti][1] - 1 == tar_idx and wordDepInfo[ti][0] == "nsubj":
                                    actor.append(wordDepInfo[ti][-1])
                                if wordDepInfo[ti][1] - 1 == tar_idx and wordDepInfo[ti][0] == "dobj" \
                                        and wordDepInfo[ti][-1] in ["您", "用户"]:
                                    actor.append(wordDepInfo[ti][-1])
                                    break
                    elif ner_label[s_idx] == "entity":
                        if not check_data(cur_tok):
                            continue
                        entity.append(cur_tok)
                    elif ner_label[s_idx] == "dataObj" and s_idx > i:
                        data.extend([cur_tok])
                    if hanlp_pos[s_idx] == "VV" and s_idx > i:
                        if cur_tok in sharingWords or cur_tok in collectWords:
                            tt = [len(t) for t in [actor, action, data, entity, neg]]
                            if tt.count(0) < 4:
                                if "服务" in data or len(data) == 0:
                                    break
                                if len(data) == 1 and data[0] == "信息":
                                    break
                                DED.append([actor, action, data, entity, neg])
                            actor = []
                            action = [cur_tok]
                            data = []
                            entity = []
                            neg = []
                            beg_flag = s_idx + 1
                            break
                # if len(data) == 1 and (not checkData(data[0])):
                #     data = []
                if not check_data(data):
                    data = []
                tt = [len(t) for t in [actor, action, data, entity, neg]]
                if tt.count(0) < 4:
                    if (not check_data(data)) or len(data) == 0:
                        continue
                    if len(data) == 1 and (not check_data(data)):
                        continue
                    data = list(set(data))
                    DED.append([actor, action, data, entity, neg])

    # 2021/11/02 如果没有DED pattern，但其实是由两个名词短语组成
    sentence = "".join(hanlp_token)
    if len(DED) == 0:
        DED = extract_use_pattern(sentence, wordDepInfo, token)
    if len(DED) == 0:
        return []
    # print("treebased:: ")
    # print("".join(hanlp_token))
    # for p in DED:
    #     s = ","
    #     for p1 in p:
    #         s += ",".join(p1) + "\t"
    #     print(s)
    return DED


def check_pattern(sen):
    if not re.match(
            r"(.*按.*本.*策略.*规定.*)|(.*按.*本.*条款.*规定.*)"
            r"|(.*按.*本.*隐私.*规定.*)|(.*按.*本.*策略.*要求.*)"
            r"|(.*按.*本.*条款.*要求.*)|(.*按.*本.*隐私.*要求.*)",
            sen) is None:
        return True
    for i in collectWords:
        mp = r"(.*如何" + i + ".*)"
        if not re.match(mp, sen) is None:
            return True

    return False


def load_customize_dictionary(file_path, model):
    tok: TaggingTokenization = model['tok/fine']
    flcd = open(file_path, 'r', encoding="utf-8")
    tmp = flcd.readlines()
    custom_dictionary = {i.split("\n")[0] for i in tmp}
    tok.dict_combine = custom_dictionary


def init_hanlp():
    hanlpmtl = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    load_customize_dictionary("Dictionary/CustimizeDictionary", hanlpmtl)
    load_customize_dictionary("Dictionary/DictionaryFromLaw", hanlpmtl)
    load_customize_dictionary("Dictionary/TPL_interested_data.txt", hanlpmtl)
    load_customize_dictionary("Dictionary/zh_TPL_list.txt", hanlpmtl)
    return hanlpmtl

def noun_merge_tree_based(token, cur_tree, han_result):
    raw_token = han_result['tok/fine']
    # cixing = han_result['pos/ctb']

    for i in cur_tree:
        if type(i) is phrasetree.tree.Tree:
            if len(i.leaves()) > 5:
                token = noun_merge_tree_based(token, i, han_result)
            elif i.label() == "NP":
                if i.leaves()[0] == "如":
                    token = noun_merge_tree_based(token, i, han_result)
                    continue
                lexicon = i.leaves()
                noun = "".join(lexicon)
                idx = locate_noun(lexicon, raw_token)
                # idx = raw_token.index(lexicon[-1])
                if idx == -1:
                    continue
                else:
                    for punc in ["，", "、", "，", "或者", "和", "或"]:
                        if punc in noun:
                            noun = noun.split(punc)[-1]
                token[idx] = noun
            elif "NP" in i.pformat_latex_qtree():
                token = noun_merge_tree_based(token, i, han_result)
                # print(tree2string(i))
                # if cixing[idx] == "NN":
                #     token[idx] = noun

    return token


def cut_sent(para):
    para = re.sub('([。。；;！？\?|||])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。。！？\?][”’])([^，。。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    # 处理a), b)，，，等情况
    para = re.sub(r'[a-z0-9]\)|[a-z0-9]）', '\n', para)
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    # while "\n\n" in para:
    #     para = para.replace("\n\n", "\n")
    return para.split("\n")


def extract_sentence_from_file(filePath: str):
    if not os.path.isfile(filePath):
        return []
    fsrc = codecs.open(filePath, "r", 'UTF-8')
    content = ""
    for line in fsrc.readlines():
        line = line.replace("|", "\n")
        line = line.replace("=", "")
        line = line.replace(" ", "")
        if line == "" or line == "\n":
            continue
        content = content + line
    fsrc.close()
    sentences = cut_sent(content)
    return sentences


def post_process_sentence(sentences: list):
    # 后处理 2021/11/01
    # 目标：将“如下信息：(1) ...”、“下列信息：(1)...”合并
    final_sentence = []
    flag_to_remove = []
    # patterns for index
    partten = r'[（一-十1-9a-z）]|[(一-十1-9a-z)]|[（一-十1-9a-z)]|[(一-十1-9a-z）]' \
              r'|[一-十1-9a-z、]|[一-十1-9a-z.]'

    for i, cur_sen in enumerate(sentences):
        if cur_sen == "":
            continue
        if len(flag_to_remove) > 0:
            flag_to_remove.pop(0)
            continue
        if "如下信息：" in cur_sen or "如下信息:" in cur_sen or "包括：" in cur_sen \
                or "包括:" in cur_sen:
            idx_tmp = min(i + 11, len(sentences))

            for z1 in range(i + 1, idx_tmp):

                if re.match(partten, sentences[z1]) is not None:
                    cur_sen = cur_sen + sentences[z1]
                    flag_to_remove.append(True)
                    # sentences.remove(sentences[z1])
        final_sentence.append(cur_sen)
    return final_sentence


def extract_dataobj_from_tree(tar_verb_idx, han_results):
    hanlp_ptree = han_results["con"]
    # tar = "记录"
    # idx = hanlp_token.index(tar)
    tree_idx = hanlp_ptree.leaf_treeposition(tar_verb_idx)
    subtree = hanlp_ptree
    for idx, num in enumerate(tree_idx[:-2]):
        subtree = subtree[num]
    noun_tree_id = tree_idx[-2] + 1
    nountree = None
    if len(subtree) > noun_tree_id:
        if subtree[noun_tree_id].label() in ["AS", "PU"]:
            if len(subtree) > tree_idx[-2] + 2:
                nountree = subtree[tree_idx[-2] + 2]
            else:
                return []
        if subtree[noun_tree_id].label() in ["NP", "NN"]:
            nountree = subtree[noun_tree_id]
    else:
        return []
    if nountree is None or not nountree.label() in ["NP", "NN"]:
        return []
    noun = []
    noun = extract_noun_subtree(nountree, noun)

    return noun


def extract_use_pattern(sentence, depInfo, tokens):
    # 2021-11-02 利用pattern 提取 DED

    data = []
    # pattern 1： 您提供的信息，并用dep info 提取 宾语的并列关系
    pattern1 = r'(.*)您(.*)[提供|存储|储存|填写](.*)信息(.*)'
    # pattern 2: “如下信息：（一）**信息 （二）**信息，。。。”
    if "如下信息：" in sentence or "如下信息:" in sentence or "包括：" in sentence \
            or "包括:" in sentence:
        # 2021/11/03 basic ideal找到 所有信息的并列名词
        for info in depInfo:
            if info[2] == "信息" and (info[0] == "nn" or info[0] == "conj"):
                data.append(tokens[info[3] - 1])
            elif info[-1] == "信息":
                data.append(tokens[info[3] - 1])
        return [[["app"], ["收集"], list(set(data)), [], []]]
    else:
        re_tmp = re.match(pattern1, sentence)
        if re_tmp is not None:
            beg_idx = re_tmp.regs[3][1]
            end_idx = beg_idx + 1
            ii = 0
            tar_idx = -1
            for idx, tok in enumerate(depInfo):
                if ii <= beg_idx and (ii + len(tok[-1])) >= end_idx:
                    tar_idx = idx
                    break
                ii = ii + len(tok[-1])
            if tar_idx == -1:
                return []
            else:
                # data.append(tok[-1])
                data.append(tokens[tar_idx])
            # 根据依赖关系找并列谓语
            data.extend(find_conj_noun(depInfo, data, idx, tokens))
            if list(set(data)) == ["信息"]:
                return []
            tmp = [[["您"], ["提供"], list(set(data)), [], []]]
            return tmp
    return []


def find_conj_noun(depInfo, data, tarIdx, tokens):
    # 根据依赖关系找并列谓语
    for z1, info in enumerate(depInfo):
        if info[1] == tarIdx and info[0] == 'conj':
            data.append(tokens[z1])
        elif info[1] == tarIdx and info[0] == 'nn':
            data.append(tokens[z1])
        elif z1 == tarIdx and info[0] == 'dep':
            data.append(tokens[info[1]-1])
            data.extend(find_conj_noun(depInfo, data, info[1], tokens))
        elif info[3] - 1 == tarIdx and info[0] == "dobj":
            # 查找同动词宾语
            # demo sentence: "您使用我们的服务时所储存的信息，如姓名、性别、出生日期、出生地、户籍所在地、民族、联系电话、收件地址、电子邮箱、联系人信息等。"
            data.extend(find_same_verb_noun(depInfo, data, info[1], tokens))
    return data


def find_same_verb_noun(depInfo, data, tarIdx, tokens):
    # 查找同动词宾语
    for z1 in range(tarIdx, len(depInfo)):
        info = depInfo[z1]
        if info[1] == tarIdx and info[0] == "dobj":
            data.append(info[-1])
            data.extend(find_conj_noun(depInfo, data, info[3], tokens))
    return list(set(data))


def extract_noun_subtree(subtree, noun: list):
    tree_str = subtree.pformat_latex_qtree()
    if not ("CC" in tree_str or "PU" in tree_str):
        return ["".join(subtree.leaves())]
    if subtree.label() in ["NP", "NN"] and len(subtree.leaves()) < 7:
        return ["".join(subtree.leaves())]
    for i in subtree:
        if type(i) is phrasetree.tree.Tree:
            if "CC" in i.pformat_latex_qtree():
                noun.extend(extract_noun_subtree(i, []))
            elif i.label() in ["NP", "NN"] and len(i.leaves()) < 7:
                noun.append("".join(i.leaves()))
            elif i.label() in ["NP", "NN"] and len(i.leaves()) >= 7:
                noun.extend(extract_noun_subtree(i, []))
            elif (not i.label() in ["NP", "NN"]) and len(i.leaves()) > 5:
                noun.extend(extract_noun_subtree(i, []))
    return noun


def check_folder(foler_path: str):
    if not os.path.exists(foler_path):
        os.mkdir(foler_path)


def check_data(token):
    if token in NOT_DATA:
        return False
    if len(inter(token, NOT_DATA)) == len(token):
        return False
    if len(token) == 1:
        token = token[0]
        if token in NOT_DATA:
            return False
        if token.endswith("权益") or token.endswith("服务") or token.endswith("能力") or token.endswith("功能") \
                or token.endswith("技术") or token.endswith("广告") \
                or token.endswith("措施") or token.endswith("手段") or token.endswith("客户端") or token.endswith("协议") \
                or token.endswith("电脑") or token.endswith("应用程序") or token.endswith("认证") or token.endswith("条款") \
                or token.endswith("政策") or token.endswith("平台") or token.endswith("公司") or token.endswith(
            "产品") or token.__contains__(
            "服务") or token.endswith("软件"):
            return False
        if token in sharingWords or token in collectWords:
            return False
    return True


def inter(a, b):
    return list(set(a) & set(b))


def locate_noun(lexicon, raw_token):
    if len(lexicon) > 1:
        for idx, i in enumerate(lexicon):
            if raw_token.count(i) == 1:
                return raw_token.index(i) + len(lexicon) - idx - 1

        for idx in range(0, len(lexicon) - 1):
            i = lexicon[idx]
            for z1 in range(raw_token.index(i), len(raw_token) - len(lexicon)):
                if raw_token[z1] == i and raw_token[z1 + 1] == lexicon[idx + 1]:
                    return z1 + len(lexicon) - idx - 1

        # for idx, i in enumerate(lexicon):
        #     for z1 in range(raw_token.index(i), len(raw_token) - len(lexicon)):
        #         if raw_token[z1] == i and raw_token[z1 + 1] == lexicon[idx + 1]:
        #             return z1 + len(lexicon) - idx - 1
    else:
        if raw_token.count(lexicon[-1]) == 1:
            return raw_token.index(lexicon[-1])

    # if raw_token.count(lexicon[-1]) == 1:
    #     return raw_token.index(lexicon[-1])
    # else:
    #     tmp = []
    # for i in lexicon:
    #     tmp.append(raw_token.index(i))
    # for i in range(len(tmp) - 1):
    #     if tmp[i + 1] - tmp[i] == 1:
    #         return tmp[i] + len(tmp) - i - 1

    return -1


def get_pccomp_subj(wordDepInfo, s_idx, hanlp_pos, token):
    actor = []
    # find the verb
    cur_dep = wordDepInfo[s_idx]
    tar_idx = cur_dep[1] - 1
    tar_pos = hanlp_pos[tar_idx]

    while tar_pos != "VV":
        cur_dep = wordDepInfo[tar_idx]
        tar_idx = cur_dep[1] - 1
        tar_pos = hanlp_pos[tar_idx]

    for i in range(0, tar_idx):
        cur_dep = wordDepInfo[i]
        if cur_dep[1] - 1 == tar_idx:
            if cur_dep[0] == "nsubj":
                actor.append(token[i])

    return actor


def is_chinese_or_punct(cur_tok):
    puncts = ["！", "？", "｡", "＂", "＃", "＄", "％", "＆", "＇", "（", "）", "＊", "＋", "，", "－", "／", "：", "；", "＜", "＝", "＞",
              "＠", "［", "＼", "］", "＾", "＿", "｀", "｛", "｜", "｝", "～", "｟", "｠", "｢", "｣", "､", "、", "〃", "》", "「", "」",
              "『", "』", "【", "】", "〔", "〕", "〖", "〗", "〘", "〙", "〚", "〛", "〜", "〝", "〞", "〟", "〰", "〾", "〿", "–", "—",
              "‘", "’", "‛", "“", "”", "„", "‟", "…", "‧", "﹏", ".",
              ")", "("]
    if cur_tok in puncts:
        return True
    else:
        return False


def get_TPL_list():
    # read TPL list file, and get a list
    tar_file = "./Dictionary/zh_TPL_list.txt"
    f = open(tar_file, 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    tpl_list = [i.replace("\n", "").replace(" ", "") for i in data]
    return list(set(tpl_list))


def get_TPL_data():
    tar_file = "Dictionary/TPL_interested_data.txt"
    f = open(tar_file, 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    data_list = [i.replace("\n", "").replace(" ", "") for i in data]
    return list(set(data_list))


def get_TPL_collect_data(tpl_list, data_list, sentence):
    z_turple = []

    for tpl in tpl_list:
        data = []
        if tpl in sentence:
            for t_data in data_list:
                if t_data in sentence:
                    data.append(t_data)

        if len(data) > 0:
            z_turple.append([[tpl], list(set(data))])
    return z_turple
