#/usr/bin/env python3
import pandas as pd
import os
import json
import fire
from copy import deepcopy

"""
call as: python3 generate_config_json.py

Read a config_master.json file and generate 
three config json files: 
1. for processing of each individual dataset: config_sim_individual_datasets.json or config_individual_datasets.json
2. for pairwise processing: config_ 
3. for all together


output:




"""

class generate_config_json():
    def __init__(self, config_filename : str, config_path : str):
        f = open(os.path.join(config_path, config_filename))
        # reading the IO_json config file
        IO_json = json.load(f)
        self.root_data_dir_name = IO_json["root_data_dir_name"]
        self.core = IO_json["core"]
        self.steps = IO_json["steps"]

        # self.output = IO_json["output"]
        self.count_datasets = len(self.core["individual"])
        self.IO_json = IO_json
        self.validate_config_file()

        # output
        self.output = { "root_data_dir_name": self.root_data_dir_name}

    def __del__(self):
        # create output directories and write dataframes to disk
        out_dir = os.path.join(self.root_data_dir_name, "generated_config")
        os.makedirs(os.path.join(out_dir), exist_ok=True)
        output_json = { "root_data_dir_name": self.root_data_dir_name}
        output_json["duplicates_pairwise"] = deepcopy(self.output["duplicates_pairwise"])
        self.save_config_json(output_json, "config_pairwise.json")
        output_json = { "root_data_dir_name": self.root_data_dir_name}
        output_json["link_all_datasets"] = deepcopy(self.output["link_all_datasets"])
        self.save_config_json(output_json, "config_all.json")


    def save_config_json(self, output_json, json_filename):
        out_dir = os.path.join(self.root_data_dir_name, "generated_config")
        with open(os.path.join(out_dir, json_filename), "w") as f:
            json.dump(output_json, f, indent=4, sort_keys=True)
        print(f"outfile created: {os.path.join(out_dir, json_filename)}")


    def validate_config_file(self):
        # check for example, that the dimension of the matrix is compatible with the number of datasets
        print(self.IO_json)

    def individual_dataset(self):
        pass

    def config_pairwise_json(self):

        self.output["duplicates_pairwise"] = dict()
        self.output["duplicates_pairwise"]["diff_svg_threshold"] = 1e-4,  # is stored as list in the output json-file. A bug in the json lib?
        self.output["duplicates_pairwise"]["IO"] = self.list_pairwise_duplicates()

    def config_all_json(self):
        """
        create a config file for the combination and aggregation of all datasets
        """

        # comment for the created config_all.json file
        self.output["link_all_datasets"] = {}
        for key in self.core:
            if "comment" in key:
                self.output["link_all_datasets"][key] = self.core[key]
        if "comment0" in self.output["link_all_datasets"]:  # let's avoid overwriting comments in the config file
            raise KeyError(f"comment0 already in config file: {self.output['link_all_datasets']['comment0']}")
        self.output["link_all_datasets"]["comment0"] = "duplicate datasets: [dir_name, file_name, human-readable label, machine-readable label, id]"
        self.output["link_all_datasets"]["individual"] = self.core["individual"]
        duplicates = [x["output"] for x in self.list_pairwise_duplicates()]
        self.output["link_all_datasets"]["duplicate"] = duplicates
        self.output["link_all_datasets"]["output"] = self.core["output"]

    def list_pairwise_duplicates(self) -> list:
        """
        return a list of the pairwise duplicates for the datasets to be written to the config file
        """
        pairwise_duplicates = []
        for i,ds in enumerate(self.core["individual"]):
            for i2, ds2 in enumerate(self.core["individual"]):
                one_pair = {}
                if i < i2:
                    one_pair["input"] = [ds, ds2]
                    one_pair["output"] = ["",f"duplicates_{ds[3]}_{ds2[3]}_per_day.csv", f"duplicates ({ds[2]}-{ds2[2]})", f"duplicates_{ds[3]}_{ds2[3]}", f"{i}-{i2}"]
                    pairwise_duplicates.append(one_pair)
        return sorted(pairwise_duplicates, key=lambda x: x["output"][3])

    def loop(self):
        """
        loop through all steps in the config file
        """
        for step in self.steps:
            if step == "individual_dataset":
                pass
            elif step == "pairwise":
                self.config_pairwise_json()
            elif step == "all":
                self.config_all_json()



def main(config_filename : str = "config_master_sim.json", config_path : str = "."):
    # print("you can run it on one duplicate plot-pair, or you run it on all of them as they are listed in config.json. See class all_duplicates.")
    ad = generate_config_json(config_filename, config_path)
    ad.loop()

if __name__ == "__main__":
    fire.Fire(main)
