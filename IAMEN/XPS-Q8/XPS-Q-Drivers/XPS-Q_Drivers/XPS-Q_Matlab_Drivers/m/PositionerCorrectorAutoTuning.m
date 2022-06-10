function [errorCode, KP, KI, KD] = PositionerCorrectorAutoTuning(socketId, PositionerName, TuningMode)
%PositionerCorrectorAutoTuning :  Astrom&Hagglund based auto-tuning
%
%	[errorCode, KP, KI, KD] = PositionerCorrectorAutoTuning(socketId, PositionerName, TuningMode)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		int32 TuningMode
%	* Output parameters :
%		int32 errorCode
%		doublePtr KP
%		doublePtr KI
%		doublePtr KD


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
KP = 0;
KI = 0;
KD = 0;

% lib call
[errorCode, PositionerName, KP, KI, KD] = calllib('XPS_Q8_drivers', 'PositionerCorrectorAutoTuning', socketId, PositionerName, TuningMode, KP, KI, KD);
