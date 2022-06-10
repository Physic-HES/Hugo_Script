function [errorCode, SinusOffset, CosinusOffset, DifferentialGain, PhaseCompensation] = PositionerEncoderCalibrationParametersGet(socketId, PositionerName)
%PositionerEncoderCalibrationParametersGet :  Read analog interpolated encoder calibration parameters
%
%	[errorCode, SinusOffset, CosinusOffset, DifferentialGain, PhaseCompensation] = PositionerEncoderCalibrationParametersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr SinusOffset
%		doublePtr CosinusOffset
%		doublePtr DifferentialGain
%		doublePtr PhaseCompensation


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
SinusOffset = 0;
CosinusOffset = 0;
DifferentialGain = 0;
PhaseCompensation = 0;

% lib call
[errorCode, PositionerName, SinusOffset, CosinusOffset, DifferentialGain, PhaseCompensation] = calllib('XPS_Q8_drivers', 'PositionerEncoderCalibrationParametersGet', socketId, PositionerName, SinusOffset, CosinusOffset, DifferentialGain, PhaseCompensation);
