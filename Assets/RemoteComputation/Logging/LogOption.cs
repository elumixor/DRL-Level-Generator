using System.Collections.Generic;
using Common;
using Common.ByteConversions;

namespace RemoteComputation.Logging
{
    public class LogOption : IByteConvertible
    {
        public int frequency;
        public int logLastN;
        public bool print;
        public bool plot;
        public bool minMax;
        public float runningAverageSmoothing;

        /// <summary> Creates a log option with the given name and parameters </summary>
        /// <param name="frequency"> How much epochs should elapse between the logging </param>
        /// <param name="logLastN">
        ///     Will only log the data for the last N epochs, if greater than zero. By default will log the data for all epochs
        /// </param>
        /// <param name="print"> Should the data be printed to the console? </param>
        /// <param name="plot"> Should the data be plotted to the graph? </param>
        /// <param name="minMax">
        ///     Should the graph also display an area for the minimum and maximum values for the epoch?
        /// </param>
        /// <param name="runningAverageSmoothing">
        ///     If greater than zero, will plot the running average of the data, with the given smoothing coefficient
        /// </param>
        public LogOption
        (int frequency = 1,
         int logLastN = 0,
         bool print = true,
         bool plot = true,
         bool minMax = true,
         float runningAverageSmoothing = 0f)
        {
            this.frequency               = frequency;
            this.logLastN                = logLastN;
            this.print                   = print;
            this.plot                    = plot;
            this.minMax                  = minMax;
            this.runningAverageSmoothing = runningAverageSmoothing;
        }

        /// <inheritdoc/>
        public IEnumerable<byte> Bytes =>
                frequency.ToBytes()
                         .ConcatMany(logLastN.ToBytes(),
                                     print.ToBytes(),
                                     plot.ToBytes(),
                                     minMax.ToBytes(),
                                     runningAverageSmoothing.ToBytes());
    }
}
