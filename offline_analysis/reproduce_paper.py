import sys
sys.path.append("../backend")
from corpus_tool import Corpus, Transcript, Visualizer

if __name__ == "__main__":
    try:
        corpus_dir = sys.argv[1]
    except:
        print("Must provide transcriptions folder path as parameter, eg: python reproduce_paper.py /Users/Ben/Documents/transcriptions")

    corpus = Corpus(corpus_dir)
    viz = Visualizer(corpus)
    for group in ["100", "200", "300", "400", "500", "600", "700"]:    
        viz.gen_dispersion(["un", "una", "unas", "unos"], group, "spa", "DET", "blue", f"imgs/determiners_time/det_{group}_spa_un_unos_una_unas.png")
        viz.gen_dispersion(["el", "la", "los", "las"], group, "spa","DET", "red", f"imgs/determiners_time/det_{group}_spa_el_los_la_las.png")
        viz.gen_dispersion(["a"], group, "eng", "DET", "blue", f"imgs/determiners_time/det_{group}_eng_a.png")
        viz.gen_dispersion(["the"], group, "eng", "DET", "red", f"imgs/determiners_time/det_{group}_eng_the.png")

    def_eng_res = viz.gen_word_boxplots(['the'], "DET", "eng", "imgs/determiners/boxplot_the_DET.png")
    print("Writing English definite article (the) boxplot to imgs/determiners/boxplot_the_DET.png")
    print("F-Statistic =", def_eng_res["ANOVA"].statistic, "p =", def_eng_res["ANOVA"].pvalue)
    print("Signifcant T-tests:", def_eng_res["significant_t-tests"])
    print("")

    indef_eng_res = viz.gen_word_boxplots(['a'], "DET", "eng", "imgs/determiners/boxplot_a_DET.png")
    print("Writing English indefinite article (a) boxplot to imgs/determiners/boxplot_a_DET.png")
    print("F-Statistic =", indef_eng_res["ANOVA"].statistic, "p =", indef_eng_res["ANOVA"].pvalue)
    print("Signifcant T-tests:", indef_eng_res["significant_t-tests"])
    print("")

    def_spa_res = viz.gen_word_boxplots(['el', 'los', 'las', 'la'], "DET", "spa", "imgs/determiners/el_los_las_la_DET_boxplot.png")
    print("Writing Spanish definite article (el/los/la/las) boxplot to imgs/determiners/el_los_las_la_DET_boxplot.png")
    print("F-Statistic =", def_spa_res["ANOVA"].statistic, "p =", def_spa_res["ANOVA"].pvalue)
    print("Signifcant T-tests:", def_spa_res["significant_t-tests"])
    print("")

    indef_spa_res = viz.gen_word_boxplots(['un', 'unos', 'una', 'unas'], "DET", "spa", "imgs/determiners/un_unos_una_unas_DET_boxplot.png")
    print("Writing Spanish indefinite article (un/unos/una/unas) boxplot to imgs/determiners/un_unos_una_unas_DET_boxplot.png")
    print("F-Statistic =", indef_spa_res["ANOVA"].statistic, "p =", indef_spa_res["ANOVA"].pvalue)
    print("Signifcant T-tests:", indef_spa_res["significant_t-tests"])
    print("")

    obj_pron_res = viz.gen_word_boxplots(['lo', 'los', 'las', 'la', 'le', 'les'], "PRON", "spa", "imgs/pronouns/le_les_lo_los_las_la_PRON_boxplot.png")
    print("Writing 3rd person object pronouns (lo/los/la/las) boxplot to imgs/pronouns/le_les_lo_los_las_la_PRON_boxplot.png")
    print("F-Statistic =", obj_pron_res["ANOVA"].statistic, "p =", obj_pron_res["ANOVA"].pvalue)
    print("Means: ", obj_pron_res["means"])
    print("Signifcant T-tests:", obj_pron_res["significant_t-tests"])
    print("")

    clitics_res = viz.gen_clitic_boxplots(False, outfile="imgs/clitics/clitics.png")
    print("Writing clitics (lo/los/la/las/le/les) boxplot to imgs/clitics/clitics.png")
    print("F-Statistic =", clitics_res["ANOVA"].statistic, "p =", clitics_res["ANOVA"].pvalue)
    print("Means: ", clitics_res["means"])
    print("Medians: ", clitics_res["medians"])
    print("Ranges: ", clitics_res["ranges"])
    print("IQRs:", clitics_res['IQRs'])
    print("Standard Deviations:", clitics_res["standard_deviations"])
    print("Signifcant T-tests:", clitics_res["significant_t-tests"])
    print("")
    
    clitics_w_pronouns_res = viz.gen_clitic_boxplots(True, outfile="imgs/clitics/clitics_w_pronouns.png")
    print("Writing clitics and 3rd person pronouns (lo/los/la/las/le/les) boxplot to imgs/clitics/clitics_w_pronouns.png")
    print("F-Statistic =", clitics_w_pronouns_res["ANOVA"].statistic, "p =", clitics_w_pronouns_res["ANOVA"].pvalue)
    print("Means: ", clitics_w_pronouns_res["means"])
    print("Medians: ", clitics_w_pronouns_res["medians"])
    print("Ranges: ", clitics_w_pronouns_res["ranges"])
    print("IQRs:", clitics_w_pronouns_res['IQRs'])
    print("Standard Deviations:", clitics_w_pronouns_res["standard_deviations"])
    print("Signifcant T-tests:", clitics_res["significant_t-tests"])