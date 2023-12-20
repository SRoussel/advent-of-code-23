"""Advent of code day 19 (part 2)."""


from functools import reduce
from collections import defaultdict
from collections import deque
import math


def lcm(a, b):
    """Return least common multiple of a and b."""
    return abs(a * b) // math.gcd(a, b)


def xnor(a, b):
    """Return a xnor b."""
    return not (a ^ b)


def nand(inputs):
    """Return nand of inputs."""
    return not reduce(lambda x, y: x and y, inputs, True)


class State:
    """Global state holder."""

    def __init__(self):
        """Init."""
        self.high_pulses = 0
        self.low_pulses = 0
        self.button_presses = 0
        self.ending_gate_button_presses = dict()


class Gate():
    """Base gate class."""

    def __init__(self, label, children, table, state):
        """Init."""
        self.label = label
        self.children = children
        self.table = table
        self.state = state

    def send_pulse(self):
        """Send the current value to children."""
        if self.children is None:
            return

        send_to = []
        for child in self.children:
            self.state.high_pulses += self.value
            self.state.low_pulses += not self.value
            if child in self.table:
                child = self.table[child]
                if child.process_pulse(self.value, self.label):
                    send_to.append(child.label)

        return send_to


class Broadcaster(Gate):
    """Broadcaster gate."""

    def __init__(self, label, children, table, state):
        """Init."""
        super(Broadcaster, self).__init__(label, children, table, state)
        self.value = False

    def process_pulse(self, pulse, _):
        """Prepare to forward pulse to children."""
        self.value = pulse
        return True


class XnorGate(Gate):
    """Xnor gate."""

    def __init__(self, label, children, table, state):
        """Init."""
        super(XnorGate, self).__init__(label, children, table, state)
        self.value = False

    def process_pulse(self, pulse, _):
        """Prepare to send xnor of pulse to children."""
        self.value = xnor(self.value, pulse)
        return not pulse


class NandGate(Gate):
    """Nand gate."""

    def __init__(self, label, children, table, state):
        """Init."""
        super(NandGate, self).__init__(label, children, table, state)
        self.inputs = defaultdict(bool)
        self.value = nand(self.inputs)

    def process_pulse(self, pulse, origin):
        """Prepare to send nand of inputs to children."""
        self.inputs[origin] = pulse
        self.value = nand(self.inputs.values())
        return True


class EndingNandGate(NandGate):
    """Ending nand gate."""

    def __init__(self, label, children, table, state):
        """Init."""
        super(EndingNandGate, self).__init__(label, children, table, state)

    def process_pulse(self, pulse, origin):
        """Prepare to send nand of inputs to children. Save if loop."""
        result = super().process_pulse(pulse, origin)

        if self.value and self.label not in self.state.ending_gate_button_presses:
            self.state.ending_gate_button_presses[self.label] = self.state.button_presses

        return result


def run(filename):
    """Return."""
    gates = dict()
    nand_gates = set()
    ending_gates = 0
    state = State()

    for line in open(filename).readlines():
        line = line.rstrip("\n")
        label, children = line.split(" -> ")
        children = children.split(", ")
        gate_type = label[0]

        if gate_type == "%":
            label = label[1:]
            gate = XnorGate(label, children, gates, state)
        elif gate_type == "&":
            label = label[1:]
            nand_gates.add(label)
            if "ql" in children:
                gate = EndingNandGate(label, children, gates, state)
                ending_gates += 1
            else:
                gate = NandGate(label, children, gates, state)
        elif gate_type == "b":
            gate = Broadcaster(label, children, gates, state)

        gates[label] = gate

    for label in nand_gates:
        for source, gate in gates.items():
            if label in gate.children:
                gates[label].inputs[source] = False

    # The first gate is the button. It sends to "broadcaster."
    start_label = "button"
    gates[start_label] = Broadcaster(start_label, ["broadcaster"], gates, state)

    while len(state.ending_gate_button_presses) < ending_gates:
        state.button_presses += 1
        start = start_label
        gates[start].process_pulse(False, "")
        gate_queue = deque()
        gate_queue.append(start)

        while len(gate_queue):
            gate = gates[gate_queue.pop()]
            children = gate.send_pulse()

            if children is not None:
                gate_queue.extendleft(filter(lambda label: label in gates, children))

    return reduce(lcm, state.ending_gate_button_presses.values(), 1)
