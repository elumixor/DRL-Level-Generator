import torch
from torch.autograd import Function


class IsGreater(Function):
    @staticmethod
    def forward(ctx, a, b, on_true, on_false):
        t = torch.tanh(a - b)
        greater = t > 0.0

        ctx.greater = greater

        ctx.save_for_backward(t)

        if greater:
            return on_true if isinstance(on_true, torch.Tensor) else torch.tensor([on_true]), torch.tensor(True)

        return on_false if isinstance(on_false, torch.Tensor) else torch.tensor([on_false]), torch.tensor(False)

    @staticmethod
    def backward(ctx, dy, _):
        s, = ctx.saved_tensors
        greater = ctx.greater
        d = 1 - s ** 2

        needs_a, needs_b, needs_on_true, needs_on_false = ctx.needs_input_grad

        da = None if not needs_a else dy * d
        db = None if not needs_b else -dy * d
        d_on_true = None if not needs_on_true else (dy if greater else None)
        d_on_false = None if not needs_on_false else (None if greater else dy)

        return da, db, d_on_true, d_on_false


is_greater = IsGreater.apply


class GreaterZero(Function):
    @staticmethod
    def forward(ctx, x, on_true, on_false):
        greater = x > 0.0

        ctx.greater = greater
        ctx.true_greater = on_true > on_false

        p_true = torch.sigmoid(x)
        ctx.save_for_backward(p_true)

        return on_true if greater else on_false

    @staticmethod
    def backward(ctx, dy):
        print(dy)

        greater = ctx.greater
        p_true, = ctx.saved_tensors

        # increase the probability of the best highest outcome
        d = p_true * (1 - p_true)
        if not ctx.true_greater:
            d *= -1

        dx = dy * d

        _, needs_on_true, needs_on_false = ctx.needs_input_grad

        d_on_true = None if not needs_on_true else (dy if greater else None)
        d_on_false = None if not needs_on_false else (None if greater else dy)

        return dx, d_on_true, d_on_false


greater_zero = GreaterZero.apply
