function [errorCode, CalibrationSinusAmplitude, CurrentSinusAmplitude, CalibrationCosinusAmplitude, CurrentCosinusAmplitude] = PositionerEncoderAmplitudeValuesGet(socketId, PositionerName)
%PositionerEncoderAmplitudeValuesGet :  Read analog interpolated encoder amplitude values
%
%	[errorCode, CalibrationSinusAmplitude, CurrentSinusAmplitude, CalibrationCosinusAmplitude, CurrentCosinusAmplitude] = PositionerEncoderAmplitudeValuesGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr CalibrationSinusAmplitude
%		doublePtr CurrentSinusAmplitude
%		doublePtr CalibrationCosinusAmplitude
%		doublePtr CurrentCosinusAmplitude


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CalibrationSinusAmplitude = 0;
CurrentSinusAmplitude = 0;
CalibrationCosinusAmplitude = 0;
CurrentCosinusAmplitude = 0;

% lib call
[errorCode, PositionerName, CalibrationSinusAmplitude, CurrentSinusAmplitude, CalibrationCosinusAmplitude, CurrentCosinusAmplitude] = calllib('XPS_Q8_drivers', 'PositionerEncoderAmplitudeValuesGet', socketId, PositionerName, CalibrationSinusAmplitude, CurrentSinusAmplitude, CalibrationCosinusAmplitude, CurrentCosinusAmplitude);
