class DatasetProcessor:
    """Handles processing and merging of datasets."""

    def __init__(self, columns):
        self.columns = columns

    def find_match(self, row, lookup_df):
        make, model, year = row["make"], row["model"], row["year"]
        match = lookup_df[(lookup_df["make"] == make) & (lookup_df["model"] == model) & (lookup_df["year"] == year)]
        return match.iloc[0].to_dict() if not match.empty else None

    def find_exist(self, row, lookup_data):
        return any(
            item["make"] == row["make"] and
            item["model"] == row["model"] and
            item["year"] == row["year"]
            for item in lookup_data
        )

    def process_rows(self, source_df, first_lookup_df, second_lookup_df, final_data):
        for _, row in source_df.iterrows():
            if self.find_exist(row, final_data):
                continue

            first_match = self.find_match(row, first_lookup_df)
            second_match = self.find_match(row, second_lookup_df)

            if first_match is not None:
                final_data.append({**row.to_dict(), **first_match})
            elif second_match is not None:
                final_data.append({**row.to_dict(), **second_match})