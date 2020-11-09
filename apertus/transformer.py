import numpy

def __default_transformer__(frame, **kwargs):
    output_frames = kwargs.get('output_frames')
    if not len(output_frames):
        return frame
    else:
        next = numpy.copy(frame)
        weight = len(output_frames)

        for row_index in range(len(next)):
            for col_index in range(len(next[row_index])):
                for chan_index in range(len(next[row_index, col_index])):
                    color = next[row_index, col_index, chan_index]
                    last_color = output_frames[-1][row_index, col_index, chan_index]
                    next[row_index, col_index, chan_index] = round((color + last_color * weight) / (weight + 1))
        return next

class Transformer:
    def __init__(self, **kwargs):
        self.input_frames = []
        self.output_frames = []
        self.transformer = kwargs.get('transformer') or __default_transformer__

    def source(self, get_frames):
        self.get_frames = get_frames
        return self

    def transform(self):
        for frame in self.get_frames():
            self.input_frames.append(frame)
            next_frame = self.transformer(frame, input_frames=self.input_frames, output_frames=self.output_frames)
            self.output_frames.append(next_frame)
            yield next_frame

    def __iter__(self):
        return self.transform()
