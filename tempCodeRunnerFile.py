        def chunks(l, n):
            count = 0
            for i in range(0, len(l), n):
                if (count < self.NoSlices):
                    yield l[i:i + n]
                    count = count + 1

        def mean(l):
            return sum(l) / len(l)

        def dataProcessing(patient, labels_df, size=10, noslices=5, visualize=False):
            label = labels_df._get_value(patient, 'cancer')
            path = self.dataDirectory + patient
            slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
            slices.sort(key=lambda x: int(x.ImagePositionPatient[2]))

            new_slices = []
            slices = [cv2.resize(np.array(each_slice.pixel_array), (size, size)) for each_slice in slices]

            chunk_sizes = math.floor(len(slices) / noslices)
            for slice_chunk in chunks(slices, chunk_sizes):
                slice_chunk = list(map(mean, zip(*slice_chunk)))
                new_slices.append(slice_chunk)

            return np.array(new_slices), label

        imageData = []
        # Check if Data Labels is available in CSV or not
        for num, patient in enumerate(self.lungPatients):
            if num % 50 == 0:
                print('Saved -', num)
            try:
                img_data, label = dataProcessing(patient, self.labels, size=self.size, noslices=self.NoSlices)
                imageData.append([img_data, label])
            except KeyError as e:
                print('Data is unlabeled')

        imageDataArray = np.array(imageData)
        np.save('imageDataNew-{}-{}-{}.npy'.format(self.size, self.size, self.NoSlices), imageDataArray)

        messagebox.showinfo("Pre-Process Data" , "Data Pre-Processing Done Successfully!") 

        self.b2["state"] = "disabled"
        self.b2.config(cursor="arrow") 
        self.b3["state"] = "normal"
        self.b3.config(cursor="hand2")
