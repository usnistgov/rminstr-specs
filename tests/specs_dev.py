"""Development script for specifications."""

if __name__ == '__main__':
    import os
    from dataclasses import dataclass

    import instruments.specifications as ispec
    import numpy as np
    from data_structures import data_record

    @dataclass
    class fake_instr:
        """Fake instrument for serials/model numbers."""

        info_dict: dict

    new_exp = True
    out_dir = os.path.join(os.getcwd(), 'specs_dev_dump\\')
    config = os.path.join(out_dir, 'config_test.csv')
    n = 10
    # %% Settings
    if new_exp:
        # make fake instruments
        dmm = fake_instr(
            {
                'serial': 'xxx',
                'model': 'HP34420A',
                'i_range': 0.01,
                'acal': True,
            }
        )

        instruments = {'V_DMM': dmm, 'I_DMM': dmm}

        # generate fake data record with my fake instruments
        dr = data_record.active_record(
            columns=['V_DMM', 'I_DMM'],
            maxlen=10000,
            output_dir=out_dir,
            meas_name='test',
            instruments=instruments,
        )

        # connect data columns to specific instruments (doing this twice to check both work)
        dr.add_instruments(instruments)

        # generate and add fake voltage/current measurements

        t = np.arange(0, n, 1)
        volt = 5 + 0.5 * np.random.random(size=n)
        curr = 6e-3 + 1e-5 * np.random.random(size=n)
        for i in range(n):
            dr.update('V_DMM', volt[i], t[i])
            dr.update('I_DMM', curr[i], t[i])

        # write data record
        dr.output()
        metadata = os.path.join(out_dir, dr.session_str + '_metadata.csv')
    else:
        # get newest metadata
        files = next(os.walk('specs_dev_dump'))[2]
        metadata_files = [f for f in files if 'metadata' in f]
        metadata = os.path.join(out_dir, metadata_files[-1])

    # %% Read in data and apply specifiction/uncertainty models
    # initialize spec manager with data record
    sm = ispec.specs_manager(metadata)

    # connect data columns to specifications
    sm.add_instruments_from_data_record(
        {'V_DMM': ispec.DatasheetMeasureDCV, 'I_DMM': None}
    )

    # function that unpacks the batch data record data into a numpy array
    def unpack(d):
        """Unpacks datarecord batch_read data into numpy array."""
        out = np.zeros((n, 2), float)
        out[:, 0] = d['V_DMM'][1]
        out[:, 1] = d['I_DMM'][1]
        return out

    # get errors
    nominal, add, names = sm.MUFmeas_from_data_record(unpack_fun=unpack)
    nominal, noadd, names = sm.MUFmeas_from_data_record(unpack_fun=unpack, add=False)
    # printing for debugging
    print('------------------------------------')
    print('Instruments Loaded into Spec Manager')
    print('------------------------------------')
    for ni in sm.instruments:
        for m in sm.instruments[ni]:
            print(sm.instruments[ni][m])

    # check nominals match
    print('------------------------------------')
    print('Value Checking')
    print('------------------------------------')
    s = 0
    for i in range(len(add)):
        s += np.sum(add[i] - nominal - noadd[i])
    print('Sum((add)-nominal-noadd) = ', s)

    print()
    # %% Actual stuff I care about
