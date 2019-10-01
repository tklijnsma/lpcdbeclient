import tables
import numpy as np
import logging
logger = logging.getLogger('root')

class EnterExitPrint(object):
    """docstring for EnterExitPrint"""
    def __init__(self, enter, exit):
        super(EnterExitPrint, self).__init__()
        self.enter = enter
        self.exit = exit
        
    def __enter__(self):
        logger.info(self.enter)

    def __exit__(self ,type, value, traceback):
        logger.info(self.exit)


def count_events(files):
    n_events = 0
    for file in files:
        f = tables.open_file(file, 'r')
        n_events += f.root.label.shape[0]
        f.close()
    return n_events


def chunks(files, chunksize, max_q_size=4, shuffle=True, max_count=None): 
    """Yield successive n-sized chunks from a and b.""" 
    i_chunk = 0
    for file in files: 
        f = tables.open_file(file, 'r') 
        nrows = f.root.label.nrows
        for istart in range(0,nrows,max_q_size*chunksize):  
            i_chunk += 1
            if max_count and i_chunk > max_count:
                break
            a = np.array(f.root.img_pt[istart:istart+max_q_size*chunksize]) # Images 
            b = np.array(f.root.label[istart:istart+max_q_size*chunksize]) # Labels 
            if shuffle: 
                c = np.c_[a.reshape(len(a), -1), b.reshape(len(b), -1)] # shuffle within queue size
                np.random.shuffle(c)
                test_images = c[:, :a.size//len(a)].reshape(a.shape)
                test_labels = c[:, a.size//len(a):].reshape(b.shape)
            else:
                test_images = a
                test_labels = b
            for jstart in range(0,len(test_labels),chunksize): 
                yield normalize_and_rgb(test_images[jstart:jstart+chunksize].copy()),test_labels[jstart:jstart+chunksize].copy(), len(test_labels[jstart:jstart+chunksize].copy())  
        f.close()


def normalize_and_rgb(images): 
    #normalize image to 0-255 per image.
    image_sum = 1/np.sum(np.sum(images,axis=1),axis=-1)
    given_axis = 0
    # Create an array which would be used to reshape 1D array, b to have 
    # singleton dimensions except for the given axis where we would put -1 
    # signifying to use the entire length of elements along that axis  
    dim_array = np.ones((1,images.ndim),int).ravel()
    dim_array[given_axis] = -1
    # Reshape b with dim_array and perform elementwise multiplication with 
    # broadcasting along the singleton dimensions for the final output
    image_sum_reshaped = image_sum.reshape(dim_array)
    images = images*image_sum_reshaped*255

    # make it rgb by duplicating 3 channels.
    images = np.stack([images, images, images],axis=-1)
    return images
    

# def eval_performance(truths, predictions, times):







