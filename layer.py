class Layer:
    def __init__(self, parallel_to_next_layer, model_number, prompt, output_destination, output_name,
                 input_destinations=None, recursive_loops=1, recursive_depth=1, conversation_output=None):
        self.parallel_to_next_layer = parallel_to_next_layer
        self.model_number = model_number
        self.prompt = prompt
        self.output_destination = output_destination
        self.output_name = output_name
        self.input_destinations = input_destinations if input_destinations is not None else []

        # --- Recursive loop settings ---
        # recursive_loops: how many times the loop group repeats. 1 = no looping (normal behavior).
        # recursive_depth: how many additional layers after this one are included in the loop group.
        #                  e.g. 1 = this layer + the next (2 agents), 2 = this layer + next 2 (3 agents).
        #                  Ignored when recursive_loops == 1.
        # conversation_output: file path where the full agent conversation is appended to each loop.
        #                       Ignored when recursive_loops == 1.
        self.recursive_loops = recursive_loops
        self.recursive_depth = recursive_depth
        self.conversation_output = conversation_output
