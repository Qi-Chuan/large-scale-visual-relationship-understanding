import csv
import tensorboardX


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class Logger(object):

    def __init__(self, path, header):
        self.log_file = open(path, 'w')
        self.logger = csv.writer(self.log_file, delimiter='\t')

        self.logger.writerow(header)
        self.header = header

    def __del(self):
        self.log_file.close()

    def log(self, values):
        write_values = []
        for col in self.header:
            assert col in values
            write_values.append(values[col])

        self.logger.writerow(write_values)
        self.log_file.flush()


def load_value_file(file_path):
    with open(file_path, 'r') as input_file:
        value = float(input_file.read().rstrip('\n\r'))

    return value


def calculate_accuracy(outputs, targets):
    batch_size = targets.size(0)

    _, pred = outputs.topk(1, 1, True)
    pred = pred.t()
    correct = pred.eq(targets.view(1, -1))
    n_correct_elems = correct.float().sum().item()

    return n_correct_elems / batch_size


class Metrics():
    def __init__(self, log_dir):
        self.summary_writer = tensorboardX.SummaryWriter(log_dir=log_dir)

    def log_metrics(self, train_metrics, val_metrics, epoch):
        train_tot_loss, train_sbj_loss, train_obj_loss, train_rel_loss, \
            train_sbj_acc, train_obj_acc, train_rel_acc = train_metrics

        val_tot_loss, val_sbj_loss, val_obj_loss, val_rel_loss, \
            val_sbj_acc, val_obj_acc, val_rel_acc = val_metrics

        # write summary
        self. summary_writer.add_scalar(
            'losses/train_tot_loss', train_tot_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'losses/train_sbj_loss', train_sbj_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'losses/train_obj_loss', train_obj_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'losses/train_rel_loss', train_rel_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'acc/train_sbj_acc', train_sbj_acc * 100, global_step=epoch)
        self.summary_writer.add_scalar(
            'acc/train_obj_acc', train_obj_acc * 100, global_step=epoch)
        self.summary_writer.add_scalar(
            'acc/train_rel_acc', train_rel_acc * 100, global_step=epoch)

        self.summary_writer.add_scalar(
            'losses/val_tot_loss', val_tot_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'losses/val_sbj_loss', val_sbj_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'losses/val_obj_loss', val_obj_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'losses/val_rel_loss', val_rel_loss, global_step=epoch)
        self.summary_writer.add_scalar(
            'acc/val_sbj_acc', val_sbj_acc * 100, global_step=epoch)
        self.summary_writer.add_scalar(
            'acc/val_obj_acc', val_obj_acc * 100, global_step=epoch)
        self.summary_writer.add_scalar(
            'acc/val_rel_acc', val_rel_acc * 100, global_step=epoch)
