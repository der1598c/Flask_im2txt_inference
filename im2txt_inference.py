""" Show and Tell inference """

# import all the needed stuffs first
import math
import os
import json

import tensorflow as tf

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary

class ShowAndTellInference(object):
    """
    Show and Tell inference class
    It needs the checkpoint file and vocabulary file
    """

    def __init__(self, checkpoint, vocab_file):
        tf.logging.set_verbosity(tf.logging.INFO)
        self.checkpoint = checkpoint
        self.vocab_file = vocab_file

        # Build the inference graph.
        self.g = tf.Graph()
        with self.g.as_default():
            self.model = inference_wrapper.InferenceWrapper()
            # Assign the checkpoint file and default configuration
            restore_fn = self.model.build_graph_from_config(configuration.ModelConfig(),
                                                self.checkpoint)
        # Finalize the graph, since we are running inference mode
        self.g.finalize()
        # Create the vocabulary.
        self.vocab = vocabulary.Vocabulary(self.vocab_file)

        # Create a Tensorflow Session and use it globally
        self.session = tf.Session(graph=self.g)
        # Load pre-trained model
        restore_fn(self.session)
        # Create caption generator
        self.generator = caption_generator.CaptionGenerator(self.model, self.vocab)

    def inference(self, img_file):
        """
        run inference against an image
        img_file is a FileStorage from Flask
        """
        # Save the image to a fixed location for this how-to
        img_file.save('/tmp/im2txt_inference.jpg')
        results = []
        # Use tf API to read to image
        with tf.gfile.GFile('/tmp/im2txt_inference.jpg', 'r') as f:
            image = f.read()

        # Use the pre-trained model to generate texts for this image
        captions = self.generator.beam_search(self.session, image)
        for __, caption in enumerate(captions):
            # Ignore begin and end words.
            sentence = [self.vocab.id_to_word(w) for w in caption.sentence[1:-1]]
            sentence = ' '.join(sentence)
            results.append({'caption': sentence, 'p': math.exp(caption.logprob)})
        # Ouput as JSON format
        return json.dumps(results)
