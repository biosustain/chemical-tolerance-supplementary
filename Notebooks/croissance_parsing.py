"""Functions for parsing the output of the croissance growth curve analysis tool"""

def calc_avg(li):
    return sum(li) / len(li)


def parse_plate_data(plate_dat, time_cutoff=None, phase_length_cutoff=5, max_slope=1.5, max_abs_baseline=0.5, max_baseline_dev=0.5, verbose=False):
    plate_res = {}
    for well_dat in plate_dat:
        well = well_dat["name"]
        times = well_dat["series"]["times"]
        ods = well_dat["series"]["values"]
        phases = well_dat["annotation"]["growthPhases"]
        good_phases = []
        for phase in phases:
            if phase["exclude"]:
                continue
            good = True

            # Check that growth rate is not unreasonably high
            if phase["slope"] > max_slope:
                if verbose:
                    print("Unreasonably high growth rate:", phase["slope"])
                good = False

            # Check that phase is long enough
            if phase["end"] - phase["start"] < phase_length_cutoff:
                if verbose:
                    print("Phase is too short:", phase["end"] - phase["start"])
                good = False

            # Check that phase starts near baseline
            start_idx = times.index(phase["start"])
            start_value_avg = calc_avg(ods[max(start_idx-3, 0): start_idx+3])
            if abs(start_value_avg - phase["baselineValue"]) > max_baseline_dev:
                if verbose:
                    print("Phase does not start at baseline:", well, start_value_avg - phase["baselineValue"])
                good = False

            # Check that baseline is not too high (or low)
            if abs(phase["baselineValue"]) > max_abs_baseline:
                if verbose:
                    print("Baseline is too high/low:", well, phase["baselineValue"])
                good = False

            if time_cutoff is not None and phase["start"] >= time_cutoff:
                if verbose:
                    print("Phase starts after time cutoff:", phase["start"])
                good = False

            if good:
                good_phases.append(phase)

        if good_phases:
            best_rank = max(phase["rank"] for phase in good_phases)
            best_index = [phase["rank"] for phase in good_phases].index(best_rank)
            best_phase = good_phases[best_index]

            plate_res[well] = {"slope": best_phase["slope"], "intercept": best_phase["intercept"],
                               "baseline": best_phase["baselineValue"], "growth": True, "start": best_phase["start"]}
        else:
            plate_res[well] = {"slope": 0, "intercept": 0, "baseline": 0, "growth": False, "start": float("nan")}

    return plate_res
